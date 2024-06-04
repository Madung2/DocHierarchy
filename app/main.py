from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from docx import Document
import json
from typing import List, Dict
app = FastAPI()

def get_alignment(paragraph):
    alignment_map = {
        0: 'left',
        1: 'center',
        2: 'right',
        3: 'justify'
    }
    return alignment_map.get(paragraph.alignment, 'unknown')

def parse_docx(file) -> List[dict]:
    document = Document(file)
    content = []
    

    for i,para in enumerate(document.paragraphs):
        font_size= 0
        bold_text= False

        # 1) font 추출
        if para.runs:
            if para.runs[0].font.size:
                font_size = para.runs[0].font.size.pt

        # 2) 정렬정보
        alignment = get_alignment(para)
        
        # 3) 단락에서 볼드텍스트 추출
        if para.runs:
            if para.runs[0].bold:
                bold_text= True


        content.append({
            "idx": i,
            "type": "paragraph",
            "font_size": font_size,
            "align_center": True if alignment =='center' else False,
            "is_bold": bold_text,
            "text": para.text
        })

    # 테이블은 일단 무시한다
    return content

def assign_levels(content: List[Dict]) -> List[Dict]:
    # 우선 font-size 기준으로 레벨을 결정합니다.

    font_sizes = sorted({item["font_size"] for item in content}, reverse=True)
    align_centers = sorted({item["align_center"] for item in content}, reverse=True)
    is_bolds = sorted({item["is_bold"] for item in content}, reverse=True)
    def calculate_level(font_size, align_center, is_bold, font_sizes=font_sizes, align_centers=align_centers, is_bolds=is_bolds):
        level = 0
        # font_size에 따른 레벨 계산
        if font_size in font_sizes:
            level += font_sizes.index(font_size)
        # align_center에 따른 레벨 계산
        if align_center in align_centers:
            level += align_centers.index(align_center)
        # is_bold에 따른 레벨 계산
        if is_bold in is_bolds:
            level += is_bolds.index(is_bold)
        return level

    # 각 paragraph에 대해 레벨 추가
    for item in content:
        item["level"] = calculate_level(item.get("font_size"), item.get("align_center"), item.get("is_bold"))
    return content



def remove_textless_content(content):
    processed_content = []
    for ele in content:
        if ele['text'] !='':
            
            processed_content.append(ele)
    return processed_content

def build_tree(content):
    # 트리 구조를 위한 스택
    stack = []
    root = {"inner_content": []}
    current_node = root
    
    for item in content:
        item["inner_content"] = []
        
        # 현재 노드보다 큰 레벨의 경우 스택에 추가
        while stack and stack[-1]["level"] >= item["level"]:
            stack.pop()
        
        # 스택이 비어있으면 루트에 추가
        if stack:
            stack[-1]["inner_content"].append(item)
        else:
            root["inner_content"].append(item)
        
        # 현재 노드를 스택에 추가
        stack.append(item)
    
    return root["inner_content"]


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return JSONResponse(content={"error": "Invalid file type"}, status_code=400)
    
    content = parse_docx(file.file)
    leveled_content = assign_levels(content)
    process_content = remove_textless_content(leveled_content) ## text없는 공백줄도 필요하면 이부분 주석처리 요망
    tree_structure = build_tree(process_content)
    return JSONResponse(content=tree_structure)
