# LangChain Examples - Comprehensive Learning Guide

A comprehensive, production-ready reference for building AI applications with **LangChain** using **Ollama** as the local language model provider. This project demonstrates everything from basic model interactions to advanced patterns like agents, tool calling, and structured outputs.

## 🎯 Project Overview

This repository provides practical, well-documented examples organized into five core learning modules:

| Module | Purpose | Files | Difficulty |
|--------|---------|-------|-----------|
| **Messages** | Fundamental message types and conversation patterns | 4 examples | ⭐ Beginner |
| **Model** | Core model capabilities from basic invocation to advanced features | 9 examples | ⭐⭐ Intermediate |
| **Tools** | Tool creation, binding, and context-aware tool management | 6 examples | ⭐⭐⭐ Advanced |
| **Agents** | Building autonomous AI agents with reasoning and tool calling | 13 examples | ⭐⭐⭐ Advanced |
| **Frontend** | UI/UX integration and generative UI patterns | Multiple examples | ⭐⭐ Intermediate |

## 🚀 Quick Start

### Prerequisites

#### 1. Install Ollama
- Download from: https://ollama.ai
- Verify installation:
  ```bash
  ollama --version
  ollama serve  # Start the Ollama service
  ```

#### 2. Python Environment (Python 3.13+)
```bash
python --version  # Verify Python 3.13 or higher
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
# or using uv (faster):
uv sync
```

#### 4. Pull Required Models
```bash
# Lightweight, balanced model (recommended for beginners)
ollama pull qwen3.5:latest

# Advanced reasoning capability
ollama pull deepseek-r1:latest

# Specialized code generation
ollama pull deepseek-coder:6.7b

# Optional: More models
ollama pull gemma2:9b
ollama pull llama2:13b
```

### Run Your First Example

```bash
cd messages
python 01_model_simpleprompt.py
```

## 📚 Module Guides

### 1. **Messages Module** - Foundations
**Location:** `messages/`

Learn how to work with LangChain message types for building conversational AI.

#### What You'll Learn
- ✅ Message types: SystemMessage, HumanMessage, AIMessage, ToolMessage
- ✅ Text prompts vs message-based prompts
- ✅ Building multi-turn conversations
- ✅ Message metadata and tracking
- ✅ Dictionary format (OpenAI compatible)

#### Examples
1. **01_model_simpleprompt.py** - Basic text prompt (simplest starting point)
2. **02_model_message.py** - Message objects for conversations
3. **03_model_message_dict_style.py** - OpenAI format compatibility
4. **04_model_message_system_persona.py** - Advanced system instructions

#### Key Concepts
```python
# Simple text prompt
response = model.invoke("Your question here")

# Message-based conversation
messages = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("Hello!"),
    AIMessage("Hi! How can I help?"),
    HumanMessage("Tell me a joke")
]
response = model.invoke(messages)

# System persona for consistent behavior
system_msg = SystemMessage("""
You are an expert Python developer.
Always provide code examples.
Explain your reasoning clearly.
""")
```

#### When to Use Each Pattern
- **Text Prompts**: Stateless requests, simple Q&A, API endpoints
- **Message Prompts**: Chatbots, stateful conversations, complex workflows
- **System Persona**: Production systems requiring consistency, specialized roles

**[Read Full Guide →](messages/README.md)**

---

### 2. **Model Module** - Capabilities
**Location:** `model/`

Comprehensive exploration of LangChain model capabilities with Ollama.

#### What You'll Learn
- ✅ Basic model invocation and streaming
- ✅ Structured outputs with Pydantic
- ✅ Tool calling and function execution
- ✅ Reasoning capabilities (DeepSeek-R1)
- ✅ Server-side tool execution
- ✅ Content block parsing

#### Examples (9 total)
1. **01_model_invoke.py** - Basic invocation and conversation
2. **02_model_stream.py** - Token streaming for real-time feedback
3. **03_model_stream_by_blocktype.py** - Parse different content types
4. **04_model_toolcalling.py** - Bind tools to models
5. **05_model_toolcalling_execution.py** - Execute tool calls
6. **06_model_structured_output_pydantic.py** - Type-safe outputs
7. **07_model_structured_output_pydantic_nestedobject.py** - Complex nested objects
8. **08_model_reasoning.py** - Advanced reasoning with DeepSeek-R1
9. **09_model_server_side_tools.py** - Server-side tool execution

#### Key Patterns
```python
# Streaming responses
for chunk in model.stream(messages):
    print(chunk.text, end="", flush=True)

# Tool calling
@tool
def get_weather(location: str) -> str:
    """Get weather for a location"""
    ...

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("What's the weather in NYC?")

# Structured output with type safety
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Model returns validated Pydantic object
response = model.invoke(
    "Extract: John, 30, Software Engineer",
    response_format=Person
)
```

**[Read Full Guide →](model/README.md)**

---

### 3. **Tools Module** - Tool Creation & Management
**Location:** `tools/`

Master tool creation, binding, and context-aware tool management for AI applications.

#### What You'll Learn
- ✅ Creating tools with the `@tool` decorator
- ✅ Type hints and automatic schema generation
- ✅ Pydantic-based input validation
- ✅ JSON schema for complex types
- ✅ Tool calling and model integration
- ✅ Accessing conversation state from tools
- ✅ Context-aware tools with user data
- ✅ Long-term memory with persistent storage
- ✅ ToolRuntime for accessing runtime information

#### Examples (6 total)
1. **01_tools_with_model.py** ⭐ - Basic tool definition and binding
2. **02_tools_with_schema_pydantic.py** ⭐⭐ - Pydantic input validation
3. **03_tools_with_schema_json.py** ⭐⭐ - JSON schema validation
4. **04_tools_stateaccess_toolruntiem.py** ⭐⭐⭐ - Access conversation state
5. **05_tools_access_context.py** ⭐⭐⭐ - User context & personalization
6. **06_tools_access_longterm_memory.py** ⭐⭐⭐ - Persistent storage across sessions

#### Key Concepts

**Basic Tool Definition:**
```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database.
    
    Args:
        query: Search terms
        limit: Max results (default: 10)
    """
    return f"Found {limit} results for '{query}'"

# Bind to model
model_with_tools = model.bind_tools([search_database])
```

**Pydantic Schema Validation:**
```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    location: str = Field(description="City name")
    units: Literal["celsius", "fahrenheit"] = Field(default="celsius")
    include_forecast: bool = Field(default=False)

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 22°{units[0].upper()}"
```

**State-Aware Tools:**
```python
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

@tool
def get_user_preference(pref_name: str, runtime: ToolRuntime) -> str:
    """Get a user preference from conversation state."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")

@tool
def update_preference(key: str, value: str, runtime: ToolRuntime) -> Command:
    """Update preference and notify model."""
    prefs = runtime.state.get("preferences", {})
    prefs[key] = value
    return Command(update={"preferences": prefs})
```

**Context-Aware Tools:**
```python
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get account for current user."""
    user_id = runtime.context.user_id
    return f"Account info for {user_id}..."
```

**Long-Term Memory (Store):**
```python
from langgraph.store.memory import InMemoryStore

@tool
def save_user_data(user_id: str, data: dict, runtime: ToolRuntime) -> str:
    """Save data to persistent store."""
    runtime.store.put(("users",), user_id, data)
    return "Saved"

@tool
def load_user_data(user_id: str, runtime: ToolRuntime) -> str:
    """Load data from persistent store."""
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Not found"
```

#### ToolRuntime - Accessing Execution Context

The `ToolRuntime` parameter provides access to:
- **`runtime.state`** - Short-term memory (conversation state)
- **`runtime.context`** - Immutable config (user IDs, session info)
- **`runtime.store`** - Long-term memory (persistent storage)
- **`runtime.stream_writer`** - Stream real-time updates
- **`runtime.execution_info`** - Thread/run IDs
- **`runtime.server_info`** - Server metadata (LangGraph Server)

#### Message Types in Tool Calling

```
User Input
    ↓
HumanMessage: "Search for customers named John"
    ↓
AIMessage: (with tool_calls to search_database)
    ↓
ToolMessage: (with search results)
    ↓
AIMessage: "I found 5 customers..."
```

#### Store Namespace Pattern

```python
# Save data
store.put(("users",), "user123", user_dict)
store.put(("conversations", "user123"), "conv_001", messages)

# Retrieve data
user_info = store.get(("users",), "user123")

# List all in namespace
all_users = store.list(("users",))
```

**Production Note:** Use `PostgresStore` for persistent storage across service restarts:
```python
from langgraph.store.postgres import PostgresStore
store = PostgresStore(connection_string="postgresql://...")
```

**[Read Full Guide →](tools/README.md)**

---

### 4. **Agents Module** - Intelligence
**Location:** `agents/`

Build autonomous AI agents that reason, plan, and use tools.

#### What You'll Learn
- ✅ Agent architecture and execution loop
- ✅ Tool binding and dynamic tool selection
- ✅ State management in agents
- ✅ Dynamic model selection based on context
- ✅ Memory and conversation history
- ✅ Agent streaming and responses
- ✅ Error handling and resilience
- ✅ Structured agent output strategies

#### Core Concepts

**Agent Loop:**
```
User Input → Reasoning (Model) → Decision → Tool Execution 
→ Observation → Reasoning → ... → Final Output
```

**Key Examples**
- `basicagent.py` - Simple agent starting point
- `agent_dynamicmodels.py` - Switch models based on task complexity
- `agent_dynamic_filtering_tools_by_state.py` - Conditional tool availability
- `agent_memory_custom_state_Schema.py` - Persistent memory management
- `agent_streaming.py` - Real-time agent output
- `agent_structured_output_tool_strategy.py` - Type-safe tool responses

#### Agent Patterns
```python
# Create a basic agent
from langchain.agents import AgentExecutor, create_openai_tools_agent

agent = AgentExecutor.from_agent_and_tools(
    agent=create_openai_tools_agent(model, tools),
    tools=tools,
    max_iterations=10
)

# Execute agent
result = agent.invoke({"input": "Your task here"})

# Streaming agent execution
for event in agent.stream({"input": "Your task"}):
    print(event)
```

**[Read Full Guide →](agents/README.md)**

---

### 5. **Frontend Module** - User Interfaces
**Location:** `frontend/`

Build interactive UIs for AI applications with generative UI patterns.

#### What You'll Learn
- ✅ Streaming responses to frontend
- ✅ Generative UI components
- ✅ Real-time updates with WebSockets
- ✅ FastAPI backend integration
- ✅ React/TypeScript frontend patterns
- ✅ State management for AI responses

#### Key Files
- `01agent_basic_frontend.py` - Backend setup for frontend communication
- `agent_generative_ui_backend.py` - Generative UI backend logic
- `AgentGenerativeUI.tsx` - React component for generative UI
- `QUICK_START.md` - Quick start guide
- `GENERATIVE_UI_GUIDE.md` - Detailed generative UI patterns

**[Read Full Guide →](frontend/README.md)**

---

## 🔧 Development Setup

### Installation

```bash
# Clone repository
git clone <repo-url>
cd langchain-examples

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
# or using uv:
uv sync
```

### Running Examples

```bash
# Using Python directly
python messages/01_model_simpleprompt.py

# Using uv (faster)
uv run messages/01_model_simpleprompt.py

# Run all examples in a module
uv run model/0*.py

# Run with environment variables
export OLLAMA_HOST=http://localhost:11434
uv run agents/basicagent.py
```

### Configuration

Create `.env` file for custom settings:
```env
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen3.5:latest
LOG_LEVEL=INFO
```

## 📋 Prerequisites Checklist

Before running examples, ensure:

- [ ] Python 3.13+ installed (`python --version`)
- [ ] Ollama installed and running (`ollama serve`)
- [ ] Required models pulled (`ollama pull qwen3.5:latest`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured (optional)

## 🐛 Troubleshooting

### Issue: "Connection refused" when running examples
**Solution:** Ensure Ollama is running
```bash
ollama serve  # In a separate terminal
```

### Issue: "Model not found" error
**Solution:** Pull the required model
```bash
ollama pull qwen3.5:latest
ollama list  # Verify installed models
```

### Issue: Out of memory (OOM) errors
**Solution:** 
1. Use smaller model: `ollama pull qwen3.5:latest` (4GB)
2. Reduce batch size in code
3. Use quantized versions of models

### Issue: Slow performance
**Solution:**
1. Ensure Ollama has adequate resources
2. Use GPU acceleration if available
3. Try a smaller model like qwen3.5

### Issue: Port already in use
**Solution:** Change Ollama port
```bash
OLLAMA_HOST=0.0.0.0:11435 ollama serve
# Update code: init_chat_model("ollama:model:tag", base_url="http://localhost:11435")
```

## 📚 Learning Path

### Beginner
1. Start with **Messages** module to understand core concepts
2. Run `messages/01_model_simpleprompt.py` first
3. Progress through message types sequentially
4. Understand conversation patterns

### Intermediate
1. Explore **Model** module (examples 1-5)
2. Learn streaming for better UX
3. Understand tool calling basics
4. Build simple chatbots

### Advanced (Choose based on needs)

**Path A: Tool & Agent Development**
1. Study **Tools** module (examples 1-3)
   - Basic tool creation with `@tool` decorator
   - Schema validation with Pydantic
   - JSON schema definitions
2. Learn state/context management in tools
3. Study **Agents** module
4. Implement agent-based systems

**Path B: State & Memory Management**
1. Study **Tools** module (examples 4-6)
   - State access via ToolRuntime
   - Context-aware tools
   - Long-term memory (Store)
2. Combine with Agents for stateful systems

### Expert
1. Explore **Frontend** module
2. Build full-stack AI applications
3. Implement advanced patterns
4. Deploy to production

---

## 🎓 LangChain Documentation References

- [LangChain Official Docs](https://docs.langchain.com)
- [Messages Guide](https://docs.langchain.com/oss/python/langchain/messages)
- [Chat Models](https://docs.langchain.com/oss/python/langchain/models)
- [Tools Documentation](https://docs.langchain.com/oss/python/langchain/tools)
- [Tool Calling Guide](https://docs.langchain.com/oss/python/langchain/models#tool-calling)
- [Agents Framework](https://docs.langchain.com/oss/python/langgraph/agents)
- [State Management](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [Structured Output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [Ollama Integration](https://docs.langchain.com/oss/python/integrations/providers/ollama)

## 📦 Project Structure

```
langchain-examples/
├── messages/              # Message types and conversation patterns
│   ├── 01_model_simpleprompt.py
│   ├── 02_model_message.py
│   ├── 03_model_message_dict_style.py
│   ├── 04_model_message_system_persona.py
│   └── README.md         # Messages module guide
│
├── model/                # Model capabilities
│   ├── 01_model_invoke.py
│   ├── 02_model_stream.py
│   ├── 03_model_stream_by_blocktype.py
│   ├── 04_model_toolcalling.py
│   ├── 05_model_toolcalling_execution.py
│   ├── 06_model_structured_output_pydantic.py
│   ├── 07_model_structured_output_pydantic_nestedobject.py
│   ├── 08_model_reasoning.py
│   ├── 09_model_server_side_tools.py
│   └── README.md         # Model module guide
│
├── agents/               # Agent patterns
│   ├── basicagent.py
│   ├── agent_*.py        # Various agent patterns
│   └── README.md         # Agent module guide
│
├── frontend/             # UI/Frontend integration
│   ├── *.py             # Backend implementations
│   ├── *.tsx            # React components
│   └── README.md        # Frontend guide
│
├── main.py              # Entry point (if applicable)
├── pyproject.toml       # Project configuration
├── README.md            # This file
└── .env                 # Configuration (create this)
```

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional model examples
- More advanced agent patterns
- Enhanced documentation
- Performance optimizations
- Bug fixes and improvements

## 📄 License

[Specify license here]

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Uses [Ollama](https://ollama.ai) for local LLM inference
- Follows LangChain best practices and patterns

## 💡 Tips for Success

1. **Start Simple**: Begin with basic examples before complex patterns
2. **Read Comments**: Each file has detailed comments explaining the code
3. **Experiment**: Modify examples to understand how things work
4. **Use Streaming**: For better UX, implement streaming in production
5. **Handle Errors**: Always implement proper error handling
6. **Track Tokens**: Monitor token usage for cost optimization
7. **Test Locally**: Test with Ollama before using cloud providers
8. **Version Control**: Keep track of working configurations

---

**Happy Learning! 🚀**

For questions or issues, check the documentation in each module or refer to the official LangChain docs.
