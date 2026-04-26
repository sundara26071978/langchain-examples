from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.agents.middleware import wrap_model_call, ModelRequest,ModelResponse


def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is always sunnyat 72°F."


def search(query: str) -> str:  
    """Search the web for a given query."""
    # This is a placeholder function. In a real implementation, this would call a search API.
    return f"Search results for {query}: ..."

simplemodel = ChatOllama(model="qwen3.5:latest")
advancedmodel = ChatOllama(model="gemma4:latest")


@wrap_model_call
def dynamic_model_selection(request:ModelRequest,handler) -> ModelResponse:
    message_count=len(request.state["messages"])
    if message_count<1:
        model=simplemodel
    else:
        model=advancedmodel
    return handler(request.override(model=model))

agent= create_agent(
    model=simplemodel, 
    tools=[get_weather,search], 
    system_prompt="you are a helpful assistant that provides weather information and can search the web.",
    middleware=[dynamic_model_selection])  

# result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Chennai?"}]})

result = agent.invoke({"messages": [{"role": "user", "content": "can you search for the latest news on AI on agent security and a related project glasswing by anthropic"},
                                    {"role": "user", "content": "What is the weather in Chennai?"}]})

print(result)

