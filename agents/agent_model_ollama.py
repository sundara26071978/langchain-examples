from langchain.agents import create_agent
from langchain_ollama import ChatOllama


def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is always sunny"


model = ChatOllama(model="gemma4:latest")

agent=create_agent(model=model, tools=[get_weather], system_prompt="you are a helpful assistant that provides weather information.")

result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Chennai?"}]})

print(result)