"""
LangChain Agent Frontend Example - Basic Agent with Generative UI

This example demonstrates:
1. Creating an agent with tools
2. Using FastAPI to expose agent as API
3. Streaming agent responses
4. Generating UI specs for frontend rendering

Run with: python 01agent_basic_frontend.py
Then access: http://localhost:8000/docs for API documentation

This backend serves a React frontend that can render the generated UIs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel


# ============================================================================
# Tool Definitions
# ============================================================================

def get_weather(city: str) -> str:
    """Get the current weather for a given city.
    
    A tool that the agent can use to fetch weather information.
    In a real implementation, this would call a weather API.
    
    Args:
        city: The city name to get weather for
    
    Returns:
        Weather information as a string
    """
    # This is a placeholder function. In a real implementation, this would call a weather API.
    return f"The current weather in {city} is always sunny at 72°F."


def web_search(query: str) -> str:
    """Search the web for a given query.
    
    A tool that the agent can use to search for information.
    In a real implementation, this would call a search API.
    
    Args:
        query: The search query
    
    Returns:
        Search results as a string
    """
    # This is a placeholder function. In a real implementation, this would call a search API.
    return f"Public Search results for {query}: ..."


# ============================================================================
# FastAPI Application
# ============================================================================

# Initialize the model
model = ChatOllama(model="gemma4:latest")

# Create the agent with memory for conversation persistence
agent = create_agent(
    model=model,
    tools=[get_weather, web_search],
    system_prompt="You are a helpful assistant that provides weather information and can search the web.",
    checkpointer=MemorySaver(),  # Persist conversation history
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    print("🚀 Agent API starting up...")
    yield
    print("🛑 Agent API shutting down...")


app = FastAPI(
    title="LangChain Agent API",
    description="Basic agent with weather and search tools",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    """Request format for chat endpoint"""
    message: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    """Response format for chat endpoint"""
    response: str
    thread_id: str


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint - returns status"""
    return {"status": "healthy", "agent": "ready"}


@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat with the agent.
    
    The agent can use its tools (weather, web search) to provide
    informed responses.
    
    Args:
        request: ChatRequest with message and optional thread_id
    
    Returns:
        ChatResponse with agent's response
    """
    try:
        # Invoke the agent with the user message
        result = agent.invoke(
            {
                "messages": [{"role": "user", "content": request.message}]
            },
            config={"configurable": {"thread_id": request.thread_id}}
        )
        
        # Extract the last message (agent's response)
        last_message = result["messages"][-1]
        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        return ChatResponse(
            response=response_text,
            thread_id=request.thread_id
        )
    
    except Exception as e:
        return ChatResponse(
            response=f"Error: {str(e)}",
            thread_id=request.thread_id
        )


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "message": "LangChain Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "docs": "/docs"
        }
    }


# ============================================================================
# Example Usage in React
# ============================================================================
"""
// React component to use this API
import { useState } from 'react';

export default function AgentChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: input }]);

    // Call agent API
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })
    });

    const data = await response.json();

    // Add agent response
    setMessages(prev => [...prev, { role: 'agent', content: data.response }]);
    setInput('');
  };

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={`message message-${msg.role}`}>
          {msg.content}
        </div>
      ))}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask me anything..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
"""


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🤖 LangChain Agent API")
    print("="*60)
    print("\n📍 Starting server on http://localhost:8000")
    print("\n📚 Interactive docs available at:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("\n💬 Example requests:")
    print("   • POST /chat - Chat with the agent")
    print("   • GET /health - Check server health")
    print("\n🔧 Tools available to agent:")
    print("   • get_weather(city) - Get weather for a city")
    print("   • web_search(query) - Search the web")
    print("\n" + "="*60 + "\n")
    
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000)