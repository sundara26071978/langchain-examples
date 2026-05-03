from langchain.tools import tool
import pprint
from langchain.chat_models import init_chat_model

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"

@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"


# Initialize the model
model = init_chat_model("ollama:qwen3.5:latest")

# Bind tools to the model
# The model now knows about search_database and can call it
model_with_tools = model.bind_tools([search_database, search])

# Ask the model something that requires tool calling
# The model will recognize it needs to call search_database
response = model_with_tools.invoke("Search for customers named John Doe")

pprint.pprint(response.content)
print("\nTool Calls Made:")
for tool_call in response.tool_calls:
    print(f"📞 Tool: {tool_call['name']}")
    print(f"   Args: {tool_call['args']}")

# Demonstrate custom tool name
print(search.name)  # web_search


