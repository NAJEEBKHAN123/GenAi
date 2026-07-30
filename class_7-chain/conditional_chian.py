from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()

# Use local Qwen model
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)

# Define two different chains for different conditions
positive_prompt = PromptTemplate(
    template='Write a thank you message for this positive feedback: {feedback}',
    input_variables=['feedback']
)

negative_prompt = PromptTemplate(
    template='Write an apology and offer help for this complaint: {feedback}',
    input_variables=['feedback']
)

parser = StrOutputParser()

positive_chain = positive_prompt | llm | parser
negative_chain = negative_prompt | llm | parser

# Condition function to check if feedback is negative
def is_negative(input_data):
    feedback = input_data['feedback'].lower()
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'disappointed']
    return any(word in feedback for word in negative_words)

# Create conditional branch using RunnableBranch
branch = RunnableBranch(
    (is_negative, negative_chain),
    positive_chain
)

# Test with positive feedback
result1 = branch.invoke({'feedback': 'I love your product, it is amazing!'})
print("Positive feedback response:", result1)

# Test with negative feedback
result2 = branch.invoke({'feedback': 'This is terrible, I hate it'})
print("\nNegative feedback response:", result2)