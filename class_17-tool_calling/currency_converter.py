from langchain_core.tools import tool, InjectedToolArg
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import json
from typing import Annotated
from dotenv import load_dotenv
import requests
import os

load_dotenv()



llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)

@tool
def get_conversion_factor(
    base_currency: str,
    target_currency: str
) -> float:
    """Fetch the conversion factor between a base currency and target currency."""

    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_RATE_API_KEY')}/latest/{base_currency.upper()}"

    response = requests.get(url)
    data = response.json()

    return data["conversion_rates"][target_currency.upper()]


conversion_result = get_conversion_factor.invoke({
    "base_currency": "USD",
    "target_currency": "PKR"
})


@tool

def convert(base_currency_value: int, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """given a currency conversion rate this function culculate the target currency value form the given base currency value"""

    return base_currency_value * conversion_rate


# print(convert.invoke({'base_currency_value': 10, 'conversion_rate': 277.5}))


#bind

llm_with_tools = llm.bind_tools([get_conversion_factor, convert])

messages = [
    HumanMessage(
        content="what is the conversion factor between USD and PKR, and based on that can you convert 10 USD to PKR"
    )
]


ai_message = llm_with_tools.invoke(messages)


for tool_call in ai_message.tool_calls:
    if tool_call['name'] == 'get_conversion_factor':
        tool_message1 = get_conversion_factor.invoke(tool_call)
        conversion_rate = json.loads(tool_message1.content)['conversion_rate']

        messages.append(tool_message1)

    if tool_call['name'] == 'convert':
        tool_call['args']['conversion_rate'] = conversion_rate
        tool_message2 = tool_call['args']['conversion_rate'] = conversion_rate
        messages.append(tool_message2)


result =  llm_with_tools.invoke(messages).content
print(result)