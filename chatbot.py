import streamlit as st
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from streamlit_annotation_tools import text_highlighter
# from dotenv import load_dotenv
from kakaotrans import Translator
translator = Translator()
# load_dotenv()

# api_key = os.getenv("OPEN_API_KEY")
client = OpenAI()
main_character = '/Users/ihoyeol/Desktop/moving/image/image5.jpeg'
llm_character = '/Users/ihoyeol/Desktop/moving/image/image1.jpeg'
situation = "당신은 어두운 동굴에 갇혔습니다. GPT의 이름은 마인입니다. GPT가 당신의 조수로서 탈출을 돕습니다. 또한 GPT는 당신에게 반말로만 대할 것이며, 친절하지는 않습니다. 또한 영어로만 대화하며 영어 단어를 쉬운 수준으로 해줘."
user_input_audio= ""
chatbot_sentences = ""

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/cBwKINB.jpg[/img]");
             background-attachment: fixed;
             background-size: cover
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

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
        st.session_state.chatbot_sentences = response

def word_translator(run_highlighter):
    all_labels = []
    unique_labels = []
    if run_highlighter:
        st.write("궁금한 단어를 선택하세요!")
        annotations = text_highlighter(st.session_state.chatbot_sentences)
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

def sentence_translator(run_translator):
    if run_translator:
        trans_sentence = translator.translate(st.session_state.chatbot_sentences, src='en', tgt='kr')
        st.write(trans_sentence)
    
st.title("동굴 탈출")

# 사이드바에 음성 입력 버튼 배치
with st.sidebar:
    st.divider()
    st.markdown("목표 1. : 불을 찾으세요.")
    st.markdown("목표 2. : 동굴을 탈출하세요.")
    st.divider()
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
            st.markdown("모험을 출발하세요!")
            st.image(main_character)
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("어떻게 할까요?"):
    chat_bot_generate()

if user_input_audio:
    prompt = user_input_audio
    # 사용자의 메시지를 세션 상태에 추가
    chat_bot_generate()

# chatbot_sentences를 st.session_state에 초기화
if 'chatbot_sentences' not in st.session_state:
    st.session_state['chatbot_sentences'] = ""

with st.sidebar:
    st.divider()
    # chatbot_sentences의 변경을 감지하고 관련 코드 실행
    with st.container():
        # st.session_state.chatbot_sentences를 사용하여 내용 표시
        st.write("답변 : ", st.session_state.chatbot_sentences)
        run_translator = st.checkbox("문장 번역이 필요하다면 클릭!")
        sentence_translator(run_translator)
        run_highlighter = st.checkbox("설명이 필요하다면 클릭!")
        word_translator(run_highlighter)


