import pprint

from langchain.agents import AgentState
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

class CustomState(AgentState):
    user_preferences: dict

model = ChatOllama(model="qwen3.5:latest ")

agent = create_agent(
    model,
    state_schema=CustomState
)
# The agent can now track additional state beyond messages
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})

pprint.pprint(result)