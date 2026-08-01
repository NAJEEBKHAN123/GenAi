from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


load_dotenv()

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokanizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokanizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe) 

# Define a lambda function to process text
def word_count(text):
    words = len(text.split())
    return f"Word count: {words}"

parser = StrOutputParser()

prompt = PromptTemplate(
    template='write a joke about {topic}',
    input_variables=['topic']
)

# Create RunnableLambda
word_counter = RunnableLambda(word_count)

# Create sequence to generate joke
joke_chain = RunnableSequence(prompt, llm, parser)

# Create parallel chain to get both joke and word count
parallel_output = RunnableParallel({
    'joke': joke_chain,
    'word_count': joke_chain | word_counter
})

# Test the lambda function
result = parallel_output.invoke({'topic': 'AI'})
print(result)