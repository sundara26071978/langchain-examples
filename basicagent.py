from langchain.agents import create_agent
from phoenix.otel import register

tracer_provider = register(
  project_name="default",
)

tracer = tracer_provider.get_tracer(__name__)

@tracer.chain
def get_weather(city:str) -> str:
    """Get the current weather for a given city."""
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is sunny with a temperature of 25°C."



agent = create_agent(model="ollama:gemma4:latest", tools=[get_weather], system_prompt="you are a helpful assistant that provides weather information.")

result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in New York?"}]})

print(result)



