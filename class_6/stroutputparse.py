from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()

# Use local Qwen model
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)

template_1 = PromptTemplate(
    template='write a details report on {topic}',
    input_variables=['topic']
)

template_2 = PromptTemplate(
    template='write a 5 lines summary of the following text. /n {text}',
    input_variables=['text']
)


prompt1 = template_1.invoke({'topic': 'black hole'})
result = llm.invoke(prompt1)
print("First result:", result)

prompt2 = template_2.invoke({'text': result})
result = llm.invoke(prompt2)
print("Summary:", result)