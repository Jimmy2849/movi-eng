from openai import OpenAI
import streamlit as st
import speech_recognition as sr


client = OpenAI(api_key="api_key")

main_character = '/Users/ihoyeol/Desktop/moving/image/image5.jpeg'
llm_character = '/Users/ihoyeol/Desktop/moving/image/image1.jpeg'

user_input_audio= ""

# 음성 입력을 위한 함수
def get_audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ko')
        st.sidebar.text(f"인식된 내용: {text}")
        return text
    except sr.UnknownValueError:
        st.sidebar.text("음성을 인식할 수 없습니다.")
        return None
    except sr.RequestError as e:
        st.sidebar.text(f"음성 인식 서비스 요청에 실패했습니다; {e}")
        return None
    
def chat_bot_generate():
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": main_character})
    with st.chat_message('user', avatar=main_character):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=llm_character):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": llm_character})

st.title("음성 챗봇")

# 사이드바에 음성 입력 버튼 배치
with st.sidebar:
    if st.button("음성으로 입력"):
        # 음성 입력 처리 로직 (여기서는 예시로 직접 함수 구현을 생략하고, 가정합니다)
        user_input_audio = get_audio_input()
                    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "character" not in st.session_state:
    st.session_state.character = {
        "name": "에코",
        "personality": "친근하고 유머러스",
        "expertise": "인공지능"
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = message.get("avatar", "default_avatar")
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    chat_bot_generate()

if user_input_audio:
    prompt = user_input_audio
    # 사용자의 메시지를 세션 상태에 추가
    chat_bot_generate()
            
