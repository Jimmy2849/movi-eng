from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

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


# # 모델 사용 예시 코드
# input_sentence = "There is many things."
# corrected_sentence = correct_grammar(input_sentence)
# print("Original:", input_sentence)
# print("Corrected:", corrected_sentence)