from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


load_dotenv()

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokanizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokanizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)


prompt1 = PromptTemplate(
    template='write a joke about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

# Lambda function to count words and return joke with count
def count_words(text):
    word_count = len(text.split())
    return f"Joke: {text}\n\nWord count: {word_count}"

# Create lambda runnable
word_counter = RunnableLambda(count_words)

chain = RunnableSequence(prompt1, llm, parser, word_counter)

result = chain.invoke({'topic': 'AI'})
print(result)