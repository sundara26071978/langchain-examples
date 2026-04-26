from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.agents.middleware import wrap_model_call, ModelRequest,ModelResponse
from typing import Callable

def public_get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is always sunnyat 72°F."

def public_search(query: str) -> str:  
    """Search the web for a given query."""
    # This is a placeholder function. In a real implementation, this would call a search API.
    return f"Private Search results for {query}: ..."

def private_search(query: str) -> str:  
    """Search the web for a given query."""
    # This is a placeholder function. In a real implementation, this would call a search API.
    return f"Private Search results for {query}: ..."

def advanced_search(query: str) -> str:  
    """Search the web for a given query."""
    # This is a placeholder function. In a real implementation, this would call a search API.
    return f"Advanced Search results for {query}: ..."

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

@wrap_model_call
def state_based_tools(request:ModelRequest,handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

    # Only enable sensitive tools after authentication
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    elif message_count < 3:
        # Limit tools early in conversation
        tools = [t for t in request.tools if t.name != "advanced_search"]
        request = request.override(tools=tools)

    return handler(request)


agent= create_agent(
    model=simplemodel, 
    tools=[public_get_weather, public_search, private_search, advanced_search],
    system_prompt="you are a helpful assistant that provides weather information and can search the web.",
    middleware=[state_based_tools,dynamic_model_selection])  

# result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Chennai?"}]})

result = agent.invoke({"messages": [{"role": "user", "content": "can you search for the latest news on AI on agent security and a related project glasswing by anthropic"},
                                    {"role": "user", "content": "What is the weather in Chennai?"}]})

print(result)

