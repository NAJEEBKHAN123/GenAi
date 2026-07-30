from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()

# Use local Qwen model
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)


prompt1 = PromptTemplate(
    template = 'generate a details report on a {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

parser = StrOutputParser()

# Sequential chain in one line
chain = prompt1 | llm | (lambda x: prompt2.invoke({'text': x})) | llm | parser

result = chain.invoke({'topic' : 'unemployment in pakistan'})

print(result)