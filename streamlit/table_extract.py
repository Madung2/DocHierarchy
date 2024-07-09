import mammoth
import re

class TableExtractor:
    def __init__(self, docx_file):
        self.docx_file = docx_file
        self.html_content = None
        self.tables = {}

    def convert_docx_to_html(self):
        result = mammoth.convert_to_html(self.docx_file)
        self.html_content = result.value

    def get_tables(self):
        # 테이블 태그를 찾아서 추출
        tables = re.findall(r'<table.*?</table>', self.html_content, re.DOTALL)
        for i, table in enumerate(tables):
            self.tables[i] = table

    def extract_tables(self):
        self.convert_docx_to_html()
        self.get_tables()
        return self.tables

# Usage example
# docx_file = "path_to_your_docx_file.docx"
# extractor = TableExtractor(docx_file)
# tables = extractor.extract_tables()
# print(tables)
