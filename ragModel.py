# 아직 사용안하는 코드!
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

def model(explanation):
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
    retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
    model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

    input_word = "Sentences using "+explanation 
    input_dict = tokenizer.prepare_seq2seq_batch(input_word, return_tensors="pt") 

    generated = model.generate(input_ids=input_dict["input_ids"]) 
    print("답변: " + tokenizer.batch_decode(generated, skip_special_tokens=True)[0]) 


model("today")
