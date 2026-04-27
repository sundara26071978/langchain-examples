from langchain_ollama import ChatOllama
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
import pprint

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

model = ChatOllama(model="qwen3.5:latest ")

agent = create_agent(
    model=model,
    response_format=ProviderStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

pprint.pprint(result["structured_response"])

# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')