from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain_ollama import ChatOllama

from agent_dynamicmodels import get_weather


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

model = ChatOllama(model="gemma4:latest")

agent=create_agent(model=model, tools=[get_weather],
                    system_prompt="you are a helpful assistant",
                    middleware=[handle_tool_errors])

result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Delhi?"}]})

print(result)