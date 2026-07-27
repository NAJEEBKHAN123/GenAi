import streamlit as st
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
model = None

# Page config
st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")
st.header("🤖 Local LLM Chat with Static Prompt")



