from langchain.tools import tool
import pprint
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput, description="Get current weather and optional forecast for a location.")
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
response = model_with_tools.invoke("What's the weather like in Paris?")
response = model_with_tools.invoke("What's the weather like in Paris with a 5-day forecast?")
pprint.pprint(response.content)
print("\nTool Calls Made:")
for tool_call in response.tool_calls:
    print(f"📞 Tool: {tool_call['name']}")
    print(f"   Args: {tool_call['args']}")

print(get_weather.description)  # Get current weather and optional forecast for a location.




