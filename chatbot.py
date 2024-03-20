import streamlit as st
from openai import OpenAI
import speech_recognition as sr
from playsound import playsound
import os

client = OpenAI(api_key="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")
main_character = '메인케릭터 이미지 파일 주소'
llm_character = 'GPT 캐릭터 이미지 파일 주소'
situation = "당신은 어두운 동굴에 갇혔습니다. GPT의 이름은 마인입니다. GPT가 당신의 조수로서 탈출을 돕습니다. 또한 GPT는 당신에게 반말로만 대할 것이며, 친절하지는 않습니다. 또한 영어로만 대화하며 영어 단어를 쉬운 수준으로 해줘."
user_input_audio= ""

def tts_openai(response):
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=response,
    )

    with open("output.mp3", "wb") as file:
        file.write(response.read())

    # 변환된 오디오 재생
    playsound("output.mp3")

    # 임시 오디오 파일 삭제
    os.remove("output.mp3")

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
    if response:
        tts_openai(response)
    
st.title("동굴 탈출")

# 사이드바에 음성 입력 버튼 배치
with st.sidebar:
    if st.button("음성으로 입력"):
        # 음성 입력 처리 로직 (여기서는 예시로 직접 함수 구현을 생략하고, 가정합니다)
        user_input_audio = get_audio_input()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": situation}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        if message["content"] == situation:
            st.markdown("모험을 시작하세요!")
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("어떻게 할까요?"):
    chat_bot_generate()

if user_input_audio:
    prompt = user_input_audio
    # 사용자의 메시지를 세션 상태에 추가
    chat_bot_generate()