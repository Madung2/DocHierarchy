from docx import Document
import json
from typing import List, Dict
import streamlit as st
import streamlit.components.v1 as components

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


# def generate_html(content):
#     html = ""
#     for ele in content:
#         level = ele['level']
#         text = ele['text']
#         is_bold = "font-weight: bold;" if ele['is_bold'] else ""
#         font_size = f"font-size: {ele['font_size']}px;" if ele['font_size'] > 0 else ""

#         # details-summary 구조 생성
#         if 'inner_content' in ele:
#             html += f"<details style='{font_size}{is_bold}'><summary>{text}</summary>\n"
#             html += generate_html(ele['inner_content'])  # 재귀 호출
#             html += "</details>\n"
#         else:
#             html += f"<p style='margin-left: {level * 20}px; {font_size}{is_bold}'>{text}</p>\n"
#     return html
# HTML 생성 함수
def generate_html(content):
    def create_html(ele):
        is_bold = "font-weight: bold;" if ele['is_bold'] else ""
        font_size = f"font-size: {ele['font_size']}px;" if ele['font_size'] > 0 else ""
        style = f"{font_size} {is_bold}"

        html = f"<div style='margin-left: {ele['level'] * 20}px; {style}'>"
        if 'inner_content' in ele:
            html += f"<span class='dropdown' onclick='toggle(this)'>{ele['text']}</span>\n"
            html += f"<div class='inner-content' style='display:none'>"
            for inner in ele['inner_content']:
                html += create_html(inner)
            html += "</div>"
        else:
            html += f"{ele['text']}"
        html += "</div>"
        return html

    html = ""
    for ele in content:
        html += create_html(ele)
    return html

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



st.title("docx 문서 구조화 모듈")
st.write("----------------------")
uploaded_file = st.file_uploader("Choose a file", type=['docx', 'doc'])
st.write("----------------------")

html_code =""
if uploaded_file is not None:
    print(uploaded_file, type(uploaded_file))
    if uploaded_file.type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        content = {"error": "Invalid file type"}
    content = parse_docx(uploaded_file)
    content = assign_levels(content)
    content = remove_textless_content(content) ## text없는 공백줄도 필요하면 이부분 주석처리 요망
    print('before_ tree', content)
    ## make html content
    html_code = generate_html(content)
    # for ele in content:
    #     level = ele['level']
    #     text = ele['text']
    #     indent = "&nbsp;" * (level * 4)  # level에 따라 들여쓰기
    #     html_code += f"<p>{indent}{text}</p>\n"
    content = build_tree(content)

else:
    content ={"hello": "World!"}


tabs = ["HTML", "JSON"]

selected_tab = st.radio('Select a tab', tabs)
if selected_tab == 'HTML':
    st.markdown(html_code, unsafe_allow_html=True)
elif selected_tab == 'JSON':
    st.json(content, expanded=True)
else:
    st.markdown(html_code, unsafe_allow_html=True)



# col1, col2 = st.columns(2)
# with col1:
# with col2:
# components.html(f"{css_code}{html_code}{js_code}", height=800, scrolling=True)