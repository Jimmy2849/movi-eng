import streamlit as st
import requests
from streamlit_local_storage import LocalStorage

url = "http://localhost:3000"  # 장고 서버 URL
app_url = '/db'


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# 로컬 스토리지 : https://pypi.org/project/streamlit-local-storage/
@st.cache_resource
def LocalStorageManager():
    return LocalStorage()
localS = LocalStorageManager()  

# 토큰 저장
def save_token(access, refresh):
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    st.session_state['token'] = access
    localS.setItem('access', access, key='access_token')
    localS.setItem('refresh', refresh, key='refresh_token')

# 토큰 불러오기
def load_token():
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    if 'access' in localS.getAll():
        st.session_state['token'] = localS.getItem('access')
        return st.session_state.token
    return

# 토큰 갱신
def refresh_token():
    if 'refesh' in localS.getAll():
        token = localS.getItem('refresh')
        response = requests.post(url + '/api/token/refresh/', data={'refresh': token})
        if response.ok:
            result = response.json()
            new_access = result['access']
            new_refresh = result['refresh']
            save_token(new_access, new_refresh)
            st.success("새로운 토큰 발급 성공")
    else:
        st.error("토큰 새로고침 실패: 유효 토큰이 없습니다.")

# 토큰 검증
# 입력된 토큰이 유효하면 empty dictionary{}를, 유효하지 않다면 {"detail", "code"}를 반환
def verify_token():
    token = load_token()
    if token:
        response = requests.post(url + '/api/token/verify/', data={'token': token})
        if response.ok:
            return True
        else:
            return False
        
def is_user_logged_in():
    # 세션 상태에 토큰이 있는지 확인하는 함수
    return 'token' in st.session_state

# 회원가입 
def userJoin():
    st.header("회원가입")
    username = st.text_input("닉네임을 입력하세요")
    password = st.text_input("비밀번호를 입력하세요", type='password')
    if st.button("가입"):
        if not username:
            st.error("닉네임을 입력해주세요.")
            return
        if not password:
            st.error("비밀번호를 입력해주세요.")
            return
        data = {'username': username, 'password': password}
        response = requests.post(url + app_url + '/signup/', data=data)

        if response.ok:
            result = response.json()
            if result.get('success'):
                st.success("회원가입이 완료되었습니다.")
            else: 
                st.error("회원가입에 실패하였습니다.")
        else:
            st.error("이미 존재하는 닉네임입니다.")

def UserLogin():
    header = st.header("로그인")
    username_input = st.empty()  # 닉네임 입력 필드를 넣을 빈 공간
    pw_input = st.empty()
    login_button = st.empty()  # 로그인 버튼을 넣을 빈 공간

    username = username_input.text_input("닉네임을 입력하세요")
    password = pw_input.text_input("비밀번호를 입력하세요", type='password')
    if login_button.button("로그인"):
        if not username:
            st.error("닉네임을 입력해주세요.")
            return
        if not password:
            st.error("비밀번호를 입력해주세요.")
            return
        data = {'username': username, 'password': password}
        response = requests.post(url + app_url + '/login/', data=data)
        if response.ok: # 상태코드가 400보다 작으면 True 반환. response.status_code로 확인.
            result = response.json()
            if result['success']:
                st.success("로그인 성공")
                token_response = requests.post(url + '/api/token/', data=data).json() # 사용자의 username를 인증정보로 갖는 jwt 토큰 발급
                print(f'발급 토큰 : {token_response}')
                save_token(token_response['access'], token_response['refresh'])
                st.success("서버에서 토큰을 성공적으로 받아와 저장했습니다.")
                st.page_link("pages/1_main_page.py", label="메인 페이지 이동", icon="👐🏻")
                username_input.empty()  # 닉네임 입력 필드 제거
                pw_input.empty() # 비밀번호 입력 필드 제거
                login_button.empty()  # 로그인 버튼 제거
                header.empty()
            else:
                st.error("존재하지 않는 이름입니다.")
        else:
            st.error("존재하지 않는 이름입니다. 회원가입을 진행해주세요.")


# 로그아웃
# def logout():
#     token = load_token_from_local_storage() # 토큰 불러오기
#     headers = {"Authorization": f"Bearer {token}"}
#     try:
#         # 서버의 /logout 엔드포인트에 GET 요청 보내기
#         response = requests.get(url + '/logout', headers=headers)

#         # 응답 상태코드 확인
#         if response.status_code == 200:
#             st.success('로그아웃되었습니다.')
#         else:
#             st.error(f'로그아웃에 실패했습니다. 상태코드: {response.status_code}')
#     except requests.RequestException as e:
#         st.error(f'로그아웃 요청 중 오류가 발생했습니다: {e}')

# def load_token_from_local_storage():
#     # 세션 상태에서 토큰을 불러오는 함수
#     return st.session_state.token if 'token' in st.session_state else None


# 메인 실행
def main():

    option = st.sidebar.selectbox(
        'Menu',
        ('로그인', '회원가입'))
    if option == '로그인':
        load_token()
        # 토큰 decode하여 username으로 authenticate 수행
        if is_user_logged_in():
            # 로그인이 되어있는 경우
            st.success("이미 로그인되었습니다.")
            st.page_link("pages/1_main_page.py", label="메인 페이지 이동", icon="👐🏻")
            if st.button("로그아웃"):
                UserLogout()
        else:
            UserLogin()
    if option == '회원가입':
        userJoin()

if __name__ == "__main__":
    main()
