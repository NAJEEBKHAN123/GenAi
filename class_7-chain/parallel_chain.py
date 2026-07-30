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

# Define prompts for parallel execution
prompt1 = PromptTemplate(
    template='Write a short poem about {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Write a 3-line joke about {topic}',
    input_variables=['topic']
)

prompt3 = PromptTemplate(
    template='Write 2 interesting facts about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

# Create parallel chains
chain1 = prompt1 | llm | parser
chain2 = prompt2 | llm | parser
chain3 = prompt3 | llm | parser

# Run chains in parallel
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    poem=chain1,
    joke=chain2,
    facts=chain3
)

# Execute all chains at once
result = parallel_chain.invoke({'topic': 'cats'})

print("Poem:", result['poem'])
print("\nJoke:", result['joke'])
print("\nFacts:", result['facts'])
