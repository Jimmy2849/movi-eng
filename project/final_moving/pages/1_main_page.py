import streamlit as st
import requests
from app import url, app_url
from streamlit_local_storage import LocalStorage

def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    session_init = st.session_state.storage_init
    keys = session_init.keys()
    if 'access' in keys:
        st.session_state.token = session_init['access']
    if 'verified' in keys:
        st.session_state.verified = session_init['verified']
    if 'userid' in keys:
        st.session_state.userid = session_init['userid']    
    return 

localS = LocalStorage()

def main_page():
    load_token_from_local_storage()
    token = st.session_state.token
    if token:
        file_path = "image/"

        logo_image1 = file_path + "Alice1.png"
        logo_image2 = file_path + "logo1.jpg"
        logo_image3 = file_path + "logo2.jpg"

        st.header("개인 페이지")

        col1, col2= st.columns(2)

        with col1:
            with st.container(height=400):
                st.image(logo_image1)
                st.page_link("pages/2_choice_story.py", label="테마 선택", icon="🐶")

        with col2:
            with st.container(height=400):
                st.image(logo_image3)
                st.page_link("pages/6_learningPage.py", label="문장 만들어보기", icon="🦊")

        st.divider()

        col1, col2, col3 = st.columns(3)
        response = requests.post(url + app_url + '/count_word/', data={'userid': st.session_state.userid})
        if response.ok:
            result = response.json()
            count_all = result['count_all']
            count_today = result['count_today']
            not_learned = result['not_learned']
            col1.metric("총 영어 단어 수 ", count_all)
            col2.metric("오늘 새로 알게 된 단어", count_today)
            col3.metric("아직 못 외운 단어", not_learned)
        else:
            col1.metric("총 영어 단어 수 ", "30")
            col2.metric("오늘 새로 알게 된 단어", "10")
            col3.metric("아직 못 외운 단어", "5")

        st.divider()

        col1, col2 = st.columns(2)
        col1.page_link("https://www.notion.so/goorm/868317501ad846009012687a07a5a4e9", label="프로젝트 페이지", icon="👜")
        col2.page_link("https://goorm.notion.site/9oormthon-Training-IN-Goorm-63fb6e888bd74e368726ba2399835a95", label="구름톤 트레이닝 페이지", icon="🧳")


if __name__ == "__main__":
    main_page()