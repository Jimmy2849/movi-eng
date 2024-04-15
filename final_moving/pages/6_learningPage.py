# 개인학습페이지
import streamlit as st
import requests
import re
import random
# from storyChat import story
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
                # st.write("단어 뜻 맞추기입니다.")
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
    # st.write(englist,kolist)
    random_en_word = random.choice(englist)
    random_ko_word = random.choice(kolist)

    col1, col2 = st.columns(2)
    with col1:
        st.info(random_en_word)
    with col2:
        st.info(random_ko_word)

    # 두 index를 비교하여 정답 확인 맞았을 경우 비슷한 문장 생성과 해설
    st.button('뜻이 서로 같습니다.')
    st.button('뜻이 서로 다릅니다.')

    




# 문장 교정
def sentenceCorrection():
    st.header("문장 교정")

def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None

# 메인 실행
def main():
    token = load_token_from_local_storage()

    if token:
        st.success("반갑습니다 :)")
        wordQuiz()
        # sentenceCorrection()

    else:
        st.warning("로컬 스토리지에 저장된 토큰이 없습니다.")
        st.write('로그인을 먼저 진행해주세요.')

if __name__ == "__main__":
    main()