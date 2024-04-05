import streamlit as st

file_path = "image/"

story_image1 = file_path + "Alice6.png"
story_image2 = file_path + "oz2.png"


def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None


def story():
        token = load_token_from_local_storage()
        if token:
             
            st.set_page_config(layout="wide")
            st.title("테마 선택")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(height=600):
                    st.image(story_image1)
                    st.subheader("이상한 나라의 앨리스")
                    st.markdown("어느 무더운 여름날, 앨리스는 나무 아래에서 책을 읽다가 말하는 토끼를 보게 됩니다. 토끼는 주머니시계를 보며 늦었다고 중얼거리며 토끼굴로 뛰어듭니다. 호기심에 가득 찬 앨리스는 토끼를 따라 토끼굴로 뛰어들어 이상한 나라에 도착합니다. 이곳에서 앨리스는 성장과 축소를 반복하며 여러 기묘한 생물들과 만나고 다양한 모험을 겪습니다. 이를 통해 그녀는 여왕의 크로켓 게임에 참가하고, 말하는 꽃들과 차 파티에 참석하는 등 다양한 경험을 합니다. 최종적으로 앨리스는 이상한 나라에서 탈출하여 현실 세계로 돌아오게 됩니다. 이야기는 앨리스가 그녀의 모험을 꿈꾸었을 뿐이라는 것으로 끝맺음됩니다.")
                st.page_link("pages/2_chatbot.py", label="스토리 선택", icon="1️⃣")


            with col2:
                with st.container(height=600):
                    st.image(story_image2)
                    st.subheader("오즈의 마법사")
                    st.markdown("어린 소녀 도로시가 캔자스 주의 집에서 사이클론에 의해 날아가 오즈라는 마법의 나라에 도착합니다. 그곳에서 그녀는 오즈의 대마법사를 만나기 위해 에메랄드 시티로 가는 황금 길을 따라가기로 결심합니다. 그녀의 여정에서 뇌가 필요한 허수아비, 심장이 필요한 양철 나무꾼, 용기가 필요한 겁쟁이 사자를 만나 함께 여행하게 됩니다. 이들은 각자의 바람을 이루기 위해 대마법사의 도움을 구하고자 합니다. 그러나 대마법사는 그들의 바람을 들어주기 위해 위험한 임무를 수행하라고 요구합니다. 임무를 완수한 후, 도로시와 그녀의 친구들은 대마법사가 실제로는 평범한 사람이라는 것을 알게 됩니다. 결국, 도로시는 좋은 마녀의 도움으로 집으로 돌아갈 방법을 찾게 됩니다. 이야기는 도로시가 가족과 함께 안전하게 집으로 돌아오며 '진정한 집보다 더 좋은 곳은 없다'는 교훈을 얻는 것으로 끝납니다.")
                st.page_link("pages/3_chatbot.py", label="스토리 선택", icon="2️⃣")

        else:
            st.warning('로그인을 먼저 진행해주세요.') 

if __name__ == "__main__":
    story()