import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

st.header("Research Tool")
user_input = st.text_input("Enter your prompt:")

if st.button("Summarize"):
    model_path = "/Users/najeeb/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
    
    with st.spinner("Loading model..."):
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    with st.spinner("Generating response..."):
        inputs = tokenizer(user_input, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    st.write(result)
