import pprint
from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

model = init_chat_model("ollama:gemma4:latest")

store = InMemoryStore()

agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo123, age: 25, email: foo123@langchain.dev"}]
})

agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc456, name: Foo456, age: 56, email: foo456@langchain.dev"}]
})

# Second session: get user info
result=agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc456'"}]
})
# Here is the user info for user with ID "abc456":
# - Name: Foo456
# - Age: 56
# - Email: foo456@langchain.dev
pprint.pprint(result)
print("Done")