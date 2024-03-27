# 개인학습페이지
import streamlit as st
import requests
import re
from page5 import page55
# from ragModel import ragmodel()

#개인 학습 페이지
# 저장된 단어 불러와서 뜻 맞추기
url = "http://localhost:3000"

# 단어 불러오기
def wordQuiz():

    if st.button('단어 불러오기'):
        token = load_token_from_local_storage() # 토큰 불러오기
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url + "/send_word", headers=headers)
            if response.status_code == 200:
                word = response.text
                st.write("단어 뜻 맞추기입니다.")
                # st.write(word)
                Quiz(word)
            else:
                # 저장된 단어가 없을 경우
                error_msg = response.json().get('error')
                st.error(error_msg)
        else:
            st.warning("로컬 스토리지에 저장된 토큰이 없습니다.")
            st.write("로그인을 먼저 진행해주세요.")    

# 단어 퀴즈 구현
def Quiz(word):
    englist=[]
    kolist=[]
    filter_word = re.sub(r'\W+|단어|뜻', ' ', word)
    filter_word = filter_word.split()
    for i in filter_word:
        if re.match(r'^[a-zA-Z]+$', i):
            englist.append(i)
        else:
            kolist.append(i)
    st.write(englist,kolist)
    # 하나씩 뽑아서 문자열로 써야지 원...


# 문장 교정
def sentenceCorrection():
    st.header("문장 교정")

def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None

# 메인 실행
def main():
    token = load_token_from_local_storage()
    if st.button("다음"):
        page55()

    if token:
        st.success("로컬 스토리지에서 토큰을 성공적으로 불러왔습니다.")
        wordQuiz()
        # sentenceCorrection()

    else:
        st.warning("로컬 스토리지에 저장된 토큰이 없습니다.")
        st.write('로그인을 먼저 진행해주세요.')

if __name__ == "__main__":
    main()