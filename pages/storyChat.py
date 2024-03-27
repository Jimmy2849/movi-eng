import streamlit as st
from Hello import text

# 테마학습 및 채팅 페이지


def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None

# 메인 실행
def story():
    token = load_token_from_local_storage()

    if token:
        st.success("로컬 스토리지에서 토큰을 성공적으로 불러왔습니다.")
        # chat()
        text()

    else:
        st.warning("로컬 스토리지에 저장된 토큰이 없습니다.")
        st.write('로그인을 먼저 진행해주세요.')

if __name__ == "__main__":
    story()
