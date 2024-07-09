

import streamlit as st
from parser import DocxParser


st.title("docx 문서 구조화 모듈")
st.write("----------------------")

uploaded_file = st.file_uploader("Choose a file", type=['docx', 'doc'])
st.write("----------------------")

html_code =""
if uploaded_file is not None:
    print(uploaded_file, type(uploaded_file))
    if uploaded_file.type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        content = {"error": "Invalid file type"}
    parser = DocxParser(uploaded_file)
    content = parser.parse()
    content = parser.assign_levels(content)
    content = parser.remove_textless_content(content)
    html_code = parser.generate_html(content)
    content = parser.get_x_pos_level(content)
    print(content)

    content = parser.build_tree(content)

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