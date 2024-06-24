import mammoth
import re

def get_tables(html):
    # 테이블 태그를 찾아서 추출
    table_dict ={}
    tables = re.findall(r'<table.*?</table>', html, re.DOTALL)
    for i, t in enumerate(tables):
        table_dict[i] =t
    return table_dict


def extract_tables_from_html(docx_file):
    result = mammoth.convert_to_html(docx_file)
    html = result.value  # HTML content extracted from the DOCX file
    # Proceed with extracting tables from the HTML content
    tables = get_tables(html)  # Assuming this function processes the HTML content
    return tables