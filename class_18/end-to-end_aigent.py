from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)


@tool
def get_weather_data(city: str) -> str:
    """Get the current weather for a city."""

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return (
        f"City: {data['name']}, "
        f"Weather: {data['weather'][0]['description']}, "
        f"Temperature: {data['main']['temp']}°C, "
        f"Humidity: {data['main']['humidity']}%"
    )


agent = create_agent(
    model=llm,
    tools=[get_weather_data],
)


result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the weather in Peshawar?"
        }
    ]
})

print(result["messages"][-1].content)