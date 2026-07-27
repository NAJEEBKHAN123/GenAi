import streamlit as st
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Page config
st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")

# Load static prompt template
static_prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Please answer the following question: {question}"
)

@st.cache_resource
def load_model():
    """Load the local Qwen model"""
    model_path = "/Users/najeeb/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
    
    st.info(f"Loading model from: {model_path}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

def main():
    st.title("🤖 Local LLM Chat with Static Prompt")
    st.write("Using Qwen2.5-0.5B-Instruct model locally")
    
    # Load model
    with st.spinner("Loading model..."):
        tokenizer, model = load_model()
    st.success("Model loaded successfully!")
    
    # User input
    question = st.text_input("Enter your question:", placeholder="What is the capital of France?")
    
    if st.button("Generate Response") and question:
        # Format the prompt
        formatted_prompt = static_prompt.format(question=question)
        
        with st.spinner("Generating response..."):
            # Tokenize input
            inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
            
            # Generate response
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode response
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
        # Display results
        st.subheader("Response:")
        st.write(response)
        
        # Show the formatted prompt
        with st.expander("View formatted prompt"):
            st.code(formatted_prompt)

if __name__ == "__main__":
    main()
