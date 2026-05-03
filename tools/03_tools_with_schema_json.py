from langchain.tools import tool
import pprint
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Literal
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result

# Initialize the model
model = init_chat_model("ollama:gemma4:latest")

# Bind tools to the model
# The model now knows about get_weather and can call it
model_with_tools = model.bind_tools([get_weather])

# Ask the model something that requires tool calling
# The model will recognize it needs to call get_weather
response = model_with_tools.invoke("What's the weather like in Paris in celsius?")
response = model_with_tools.invoke("What's the weather like in Paris in celsius with a 5-day forecast?")
pprint.pprint(response.content)
print("\nTool Calls Made:")
for tool_call in response.tool_calls:
    print(f"📞 Tool: {tool_call['name']}")
    print(f"   Args: {tool_call['args']}")

print(get_weather.description)  # Get current weather and optional forecast for a location.




