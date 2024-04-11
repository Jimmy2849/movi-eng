from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 모델 및 토크나이저 로드
model_path = "baristarules/gec-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# GPU 사용 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def correct_grammar(input_sentence):

    inputs = tokenizer(input_sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)

    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=512)
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_sentence

database_word = 'work'

llm = OpenAI()

st.title("문장 만들어보기")

content = st.text_input("단어를 입력해주세요.")

if st.button("예시 문장 만들기"):
    result = llm.predict("Make 2 short and simple English sentences using" + content)
    st.text(result)

st.divider()
input_sentence = st.text_input("단어를 이용해 문장을 만들어보세요.")

if st.button("문장 교정"):
    corrected_sentence = correct_grammar(input_sentence)
    st.text("Original:" + input_sentence)
    st.text("Corrected:" + corrected_sentence)
