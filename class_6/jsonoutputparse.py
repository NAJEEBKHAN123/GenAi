from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

# Use local Qwen model
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

#Create pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)

Parser = JsonOutputParser()

template = PromptTemplate(
    template='Give ma a name, age and city of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction': Parser.get_format_instructions()}
)


chain = template | llm | Parser

result = chain.invoke({})

print(result)

