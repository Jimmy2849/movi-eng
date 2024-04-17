from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import streamlit as st
from langchain.llms import OpenAI

import streamlit as st
import requests
import re
import random



# 모델 및 토크나이저 로드
model_path = "baristarules/gec-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# GPU 사용 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# 저장된 단어 불러와서 뜻 맞추기
url = "http://localhost:3000"

# 문장 교정 불러오기
def correct_grammar(input_sentence):

    inputs = tokenizer(input_sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)

    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)

    outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=512)
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_sentence

# 단어 불러오기 및 문장 생성
def wordQuiz():
    
    st.title("단어 학습장")

    token = load_token_from_local_storage() # 토큰 불러오기
    if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url + "/send_word", headers=headers)
            if response.status_code == 200:
                word = response.text        
                Quiz(word)
                
                sentence()

                
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

    if 'word_index' not in st.session_state:
        st.session_state['word_index'] = []

    en_random_index = random.randint(0, min(len(englist), len(kolist)) - 1)
    ko_random_index = random.randint(0, min(len(englist), len(kolist)) - 1)
    
    if st.button('다음 단어'):
        st.session_state.word_index.append((englist[en_random_index], kolist[ko_random_index], en_random_index, ko_random_index))
        if len(st.session_state.word_index) > 2:
            st.session_state.word_index.pop(0)
    


    col1, col2 = st.columns(2)
    with col1:
        try:
            st.info(st.session_state.word_index[0][0])
        except IndexError:
            pass
            


    with col2:
        try:
            st.info(st.session_state.word_index[0][1])
        except IndexError:
            pass



    genre = st.checkbox('단어의 뜻이 서로 같습니다.')
    no_genre = st.checkbox('단어의 뜻이 서로 다릅니다.')

    if genre:
        if st.session_state.word_index[0][2] == st.session_state.word_index[0][3]:
         st.success(f'정답입니다! {st.session_state.word_index[0][0]}는 "{st.session_state.word_index[0][1]}" 의미를 가지고 있습니다')
        else:
            st.warning(f'아쉬워요.. 다시 잘 생각해보세요')
    
    if no_genre:
        if st.session_state.word_index[0][2] != st.session_state.word_index[0][3]:
         st.success(f'정답입니다! {st.session_state.word_index[0][0]}는 "{st.session_state.word_index[0][1]}" 의미를 가지고 있습니다')
        else:
            st.warning(f'아쉬워요.. 다시 잘 생각해보세요')
    



# 문장 교정
def sentence():

    llm = OpenAI(api_key="")
    st.header("문장 교정")

    # st.divider()
    input_sentence = st.text_input("위 단어를 가지고 문장을 만들어 보세요!")

    on = st.toggle('도움이 필요하신가요?')
    if on:
        st.write('다음 문장을 활용해 보세요!')
        result = st.session_state.word_index[0][0]
        result = llm.predict("Make 1 short and simple English sentences using" + result)
        st.text(result)

    if st.button("문장 교정"):
        corrected_sentence = correct_grammar(input_sentence)
        st.text("Original:" + input_sentence)
        st.text("Corrected:" + corrected_sentence)

def load_token_from_local_storage():
    # 세션 상태에서 토큰을 불러오는 함수
    return st.session_state.token if 'token' in st.session_state else None

# 메인 실행
def main():
    token = load_token_from_local_storage()

    if token:
        wordQuiz()
        # sentence()
            
    else:
        st.warning("로컬 스토리지에 저장된 토큰이 없습니다.")
        st.write('로그인을 먼저 진행해주세요.')

if __name__ == "__main__":
    main()