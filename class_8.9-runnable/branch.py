from langchain_community.llms import HuggingFacePipeline
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import  RunnableSequence, RunnableBranch, RunnablePassthrough
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


load_dotenv()

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokanizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokanizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe) 

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='write a details report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='summary of the following text {text}',
    input_variables=['text']
)

report_chain = RunnableSequence(prompt1, llm, parser)

# Condition function to check if text is longer than 300 words
def is_long_text(text):
    return len(text.split()) > 300

branch_chain = RunnableBranch(
    (is_long_text, RunnableSequence(prompt2, llm, parser)),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_chain, branch_chain)

final = final_chain.invoke({'topic': 'Russia vs Ukraine'})
print(final)
