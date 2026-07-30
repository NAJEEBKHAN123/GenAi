from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()

# Use local Qwen model
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)


class Person(BaseModel):
    name: str = Field(description="The full name of the person")
    age: int = Field(description="The age of the person")
    city: str = Field(description="The city of the person")


parser = PydanticOutputParser(pydantic_object=Person)


template = PromptTemplate(
    template='generate the name, age and city of the fictional {place} \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)


chain = template | llm | parser

result = chain.invoke({'place': 'Pakistan'})

print(result)