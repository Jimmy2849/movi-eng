import streamlit as st
from streamlit_chat import message
from streamlit_annotation_tools import text_highlighter
from kakaotrans import Translator
import requests

# 번역기 초기화
translator = Translator()
url = "http://localhost:3000"

def display_message(text):
    message(text)

def highlight_text(text):
    st.write("궁금한 단어를 선택하세요!")
    annotations = text_highlighter(text)
    all_labels = []
    unique_labels = []
    
    if annotations is not None and len(annotations) > 0:
        for sublist in annotations:
            if sublist:
                all_labels.extend([item["label"] for item in sublist])

        # 중복 제거를 위해 set으로 변환 후 다시 리스트로 변환
        unique_labels = list(set(all_labels))
        st.write("Unique Labels:", unique_labels)
    else:
        st.write("Annotations이 비어 있습니다.")
    
    return unique_labels

def translate_labels(labels):
    material_result_list = []
    for material in labels:
        material_result_list.append(translator.translate(material, src='en', tgt='kr'))

    return material_result_list

def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None

# 단어 저장 함수
def save_word(data):
    token = load_token_from_local_storage()  # 토큰 불러오기
    headers = {'Authorization': f'Bearer {token}'}
    if st.button('저장'):
        response = requests.post(url + '/save_word', data=data, headers=headers)


# 메인 실행
def text():
    message("Hello bot!", is_user=True)  # align's the message to the right

    text = "Your future is shaped by how you act today. Pay more attention to challenges than to fears."
    display_message(text)

    run_highlighter = st.checkbox("설명이 필요하다면 클릭!")
    if run_highlighter:
        unique_labels = highlight_text(text)
        translated_labels = translate_labels(unique_labels)
        st.write("번역된 결과:", translated_labels)

        word = unique_labels
        meaning = translated_labels
        data = {'word' : word, 'meaning': meaning}
        save_word(data)

