import streamlit as st
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import base64
from streamlit_annotation_tools import text_highlighter
# from dotenv import load_dotenv
from kakaotrans import Translator
translator = Translator()
# load_dotenv()

# api_key = os.getenv("OPEN_API_KEY")
client = OpenAI()
main_character = '/Users/ihoyeol/Desktop/moving/image/image5.jpeg'
llm_character = '/Users/ihoyeol/Desktop/moving/image/image1.jpeg'
goal1_image_path = "/Users/ihoyeol/Desktop/moving/image/fire.jpeg"
goal2_image_path = "/Users/ihoyeol/Desktop/moving/image/forest.jpeg"

situation = "The username is Dorothy and the gpt's name is The Tin Woodman. You are currently trapped in a cave and you must help Dorothy escape from it. There are two goals: 1. Start a fire in the cave. 2. Escape the cave. Here, if you have achieved goal 1, please tell me the answer that includes 'AAA' at the end of the sentence only once. If you have achieved goal 2, tell me the answer that includes 'BBB' at the end of the sentence only once. Please use a friendly tone, speak only in English, and do not answer longer than two sentences."
user_input_audio= ""
chatbot_sentences = ""

def decrease_count():
    if st.session_state.count > 0:
        st.session_state.count -= 1

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
        
    # 응답 생성 및 필터링을 한 번의 with 블록 내에서 처리합니다.
    with st.chat_message("assistant", avatar=llm_character):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        # "AAA"와 "BBB"를 필터링합니다.
        filtered_response = response.choices[0].message.content.replace("AAA", "").replace("BBB", "")
        st.markdown(filtered_response)
        st.session_state.filtered_response = filtered_response
    
    # 필터링된 응답을 세션 상태 메시지에 추가합니다.
    st.session_state.messages.append({"role": "assistant", "content": filtered_response, "avatar": llm_character})

    if response:
        tts_openai(filtered_response)
        st.session_state.chatbot_sentences = response.choices[0].message.content
        if "AAA" in st.session_state.chatbot_sentences:
            goal_sentence = "1번 목표를 달성하였습니다."
            st.session_state.messages.append({"role": "system", "content" : goal_sentence})
            with st.chat_message('system'):
                st.markdown(goal_sentence)
                st.image(goal1_image_path)
                st.toast(goal_sentence)
        elif "BBB" in st.session_state.chatbot_sentences:
            goal_sentence = "2번 목표를 달성하였습니다."
            st.session_state.messages.append({"role": "system", "content" : goal_sentence})
            with st.chat_message('system'):
                st.markdown(goal_sentence)
                st.image(goal2_image_path)
                st.toast(goal_sentence)
                st.balloons()

def word_translator(run_highlighter):
    all_labels = []
    unique_labels = []
    if run_highlighter:
        st.write("궁금한 단어를 선택하세요!")
        annotations = text_highlighter(st.session_state.filtered_response)
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
        trans_sentence = translator.translate(st.session_state.filtered_response, src='en', tgt='kr')
        st.write(trans_sentence)
    
st.title("동굴 탈출")

if 'count' not in st.session_state:
        st.session_state.count = 5 

if 'filtered_response' not in st.session_state:
    st.session_state.filtered_response = ""

# 사이드바에 음성 입력 버튼 배치
with st.sidebar:
    st.write(f'현재 카운트: {st.session_state.count} / 5')
    st.divider()
    st.markdown("목표 1. : 불을 찾으세요.")
    st.markdown("목표 2. : 동굴을 탈출하세요.")
    st.divider()
    if st.button("음성으로 입력"):
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
            st.image('/Users/ihoyeol/Desktop/moving/image/cave.jpeg')
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("어떻게 할까요?"):
    chat_bot_generate()
    decrease_count()

if user_input_audio:
    prompt = user_input_audio
    chat_bot_generate()
    decrease_count()

# chatbot_sentences를 st.session_state에 초기화
if 'chatbot_sentences' not in st.session_state:
    st.session_state['chatbot_sentences'] = ""

with st.sidebar:
    st.divider()
    # chatbot_sentences의 변경을 감지하고 관련 코드 실행
    with st.container():
        # st.session_state.chatbot_sentences를 사용하여 내용 표시
        st.write("답변 : ", st.session_state.filtered_response)
        run_translator = st.checkbox("문장 번역이 필요하다면 클릭!")
        sentence_translator(run_translator)
        run_highlighter = st.checkbox("설명이 필요하다면 클릭!")
        word_translator(run_highlighter)


