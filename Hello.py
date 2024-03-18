import streamlit as st
from streamlit_chat import message
from streamlit_annotation_tools import text_highlighter

from kakaotrans import Translator
translator = Translator()

message("Hello bot!", is_user=True)  # align's the message to the right

text = "Your future is shaped by how you act today. Pay more attention to challenges than to fears."

# 체크박스를 생성하여 체크 여부에 따라 text_highlighter 함수 실행 여부를 결정
with st.container():
    message(text)
    run_highlighter = st.checkbox("설명이 필요하다면 클릭!")

    all_labels = []
    unique_labels = []
    if run_highlighter:
        st.write("궁금한 단어를 선택하세요!")
        annotations = text_highlighter(text)
        if annotations is not None and len(annotations) > 0:
            for sublist in annotations:
                if sublist:
                    all_labels.extend([item["label"] for item in sublist])

            # 중복 제거를 위해 set으로 변환 후 다시 리스트로 변환
            unique_labels = list(set(all_labels))
            st.write("Unique Labels:", unique_labels)
        else:
            st.write("Annotations이 비어 있습니다.")

material_list = unique_labels
material_result_list = []

# 영어로 번역
for material in material_list:
    material_result_list.append(translator.translate(material, src='en', tgt='kr'))


st.write("번역된 결과:", material_result_list)
