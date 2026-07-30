from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


load_dotenv()

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokanizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokanizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)


prompt1 = PromptTemplate(
    template='Generate a tweet about {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a post for linkedin {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

chain = RunnableParallel({
        'tweet' : RunnableSequence(prompt1, llm, parser),
        'linkedin' : RunnableSequence(prompt2, llm, parser)
    })

result = chain.invoke({'topic': 'cat'})
print(result)