from dataclasses import dataclass
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.agents.middleware import wrap_model_call, ModelRequest,ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_role: str


model = ChatOllama(model="qwen3.5:latest")
@wrap_model_call
def context_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Runtime Context permissions."""
    # Read from Runtime Context: get user role
    if request.runtime is None or request.runtime.context is None:
        # If no context provided, default to viewer (most restrictive)
        user_role = "viewer"
    else:
        user_role = request.runtime.context.user_role

    if user_role == "admin":
        # Admins get all tools
        pass
    elif user_role == "editor":
        # Editors can't delete
        tools = [t for t in request.tools if t.name != "delete_data"]
        request = request.override(tools=tools)
    else:
        # Viewers get read-only tools
        tools = [t for t in request.tools if t.name.startswith("read_")]
        request = request.override(tools=tools)

    return handler(request)



# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.
store = InMemoryStore()

# Write sample data to the store using the put method
store.put(
    (
        "features",
    ),  # Namespace to group related data together (users namespace for user data)
    "user_123",  # Key within the namespace (user ID as key)
    {
        "user_id" : "user_123",
        "name": "Sundara",
        "enabled_tools": ["public_get_weather", "private_search"],
    },  # Data to store for the given user
)
def read_data(key: str) -> str:
    """Read data for a given key."""
    return f"Reading data for {key}..."

def write_data(key: str, value: str) -> str:
    """Write data for a given key."""
    return f"Writing data for {key}: {value}..."

def delete_data(key: str) -> str:
    """Delete data for a given key."""
    return f"Deleting data for {key}..."



agent= create_agent(
    model=model, 
     tools=[read_data, write_data, delete_data],
    system_prompt="you are a helpful assistant that provides weather information and can search the web.",
    middleware=[context_based_tools],
  
    context_schema=Context  
  
)
context=Context(user_role="viewer")
# context=Context(user_role="editor")
# context=Context(user_role="Admin")


result = agent.invoke({"messages": [
                                    {"role": "user", "content": "read data for key1"},
                                    {"role": "user", "content": "Write data for key1 with value 'hello'"},
                                    # {"role": "user", "content": "Delete data for key1"}
                                    ]},
                    context=context                
                    )

print(result)

