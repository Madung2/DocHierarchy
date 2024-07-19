

import os
import streamlit as st
from parser import DocxParser
from converter.docx_converter import convert_to_docx


st.title("docx 문서 구조화 모듈")
st.write("----------------------")

uploaded_file = st.file_uploader("Choose a file", type=['docx', 'doc', 'hwp'])
st.write("----------------------")

html_code = ""
content = {}
if uploaded_file is not None:
    print(uploaded_file, type(uploaded_file))

    # Create temp directory if it doesn't exist
    temp_dir = os.path.join("/shared_data", "streamlit", "converter", "converted_files")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save uploaded file to a temporary location in shared_data
    shared_data_input_file = os.path.join(temp_dir, uploaded_file.name)
    with open(shared_data_input_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    output_dir = temp_dir

    # Check file type and convert if necessary
    print('type', uploaded_file.type)
    if uploaded_file.type in ["application/x-hwp", "application/haansofthwp"]:
        # Convert the file if it's a HWP file
        shared_data_input_file = convert_to_docx(shared_data_input_file, output_dir)

    # Check if the file is a valid DOCX file
    if not shared_data_input_file.endswith(".docx"):
        content = {"error": "Invalid file type"}
    else:
        parser = DocxParser(shared_data_input_file)
        content = parser.parse()
        content = parser.assign_levels(content)
        content = parser.remove_textless_content(content)
        ### tab 위치 지정
        content = parser.get_x_pos_level(content)
        parser.put_table_level(content)
        ### tab 위치 지정
        html_code = parser.generate_html(content)
        print(content)

        content = parser.build_tree(content)

else:
    content = {"hello": "World!"}

tabs = ["HTML", "JSON"]

selected_tab = st.radio('Select a tab', tabs)
if selected_tab == 'HTML':
    st.markdown(html_code, unsafe_allow_html=True)
elif selected_tab == 'JSON':
    st.json(content, expanded=True)
else:
    st.markdown(html_code, unsafe_allow_html=True)