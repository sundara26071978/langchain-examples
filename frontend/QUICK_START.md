# 🎨 LangChain Generative UI - Quick Start Guide

## What You've Got

You now have a complete Generative UI setup with:
- **Backend API** (`01agent_basic_frontend.py`) - LangChain agent with tools
- **Generative UI Backend** (`agent_generative_ui_backend.py`) - Advanced agent with UI generation
- **React Frontend** (`AgentGenerativeUI.tsx`) - Full-featured React component
- **Comprehensive Guide** (`GENERATIVE_UI_GUIDE.md`) - Deep dive into concepts

## 🚀 Quick Start (5 minutes)

### Step 1: Run the Backend

```bash
# Terminal 1: Run the basic agent API
cd frontend
python 01agent_basic_frontend.py

# You should see:
# 🤖 LangChain Agent API
# 📍 Starting server on http://localhost:8000
# 📚 Interactive docs available at: http://localhost:8000/docs
```

### Step 2: Test the API

Open http://localhost:8000/docs in your browser to see interactive API docs (Swagger UI).

**Try this request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the weather in New York?"
  }'
```

**Expected response:**
```json
{
  "response": "The current weather in New York is always sunny at 72°F.",
  "thread_id": "default"
}
```

### Step 3: Run Generative UI Backend (Optional)

```bash
# Terminal 2: Run the advanced Generative UI agent
python agent_generative_ui_backend.py

# Available at: http://localhost:8000/docs
```

### Step 4: Connect React Frontend

```bash
# In your React project:
npm install @json-render/react zod

# Copy AgentGenerativeUI.tsx to your components folder
# Import and use: <AgentGenerativeUI />
```

## 📊 Understanding the Flow

### Basic Agent (01agent_basic_frontend.py)

```
User Input
    ↓
POST /chat
    ↓
Agent processes message
    ↓
Uses tools: get_weather, web_search
    ↓
Returns text response
    ↓
Frontend displays in chat
```

**Best for:** Regular chat, tools that return text

### Generative UI Agent (agent_generative_ui_backend.py)

```
User Input: "Create a login form"
    ↓
POST /agent/chat
    ↓
Agent understands component catalog
    ↓
Generates JSON UI spec
    ↓
Frontend renders interactive form
    ↓
User can interact with form
```

**Best for:** Generating interactive UIs, dynamic forms, dashboards

## 🎯 Common Tasks

### 1. Add a New Tool to the Agent

**In `01agent_basic_frontend.py`:**

```python
def calculate_distance(location1: str, location2: str) -> str:
    """Calculate distance between two locations."""
    return f"Distance from {location1} to {location2}: ~100 miles"

# Add to agent
agent = create_agent(
    model=model,
    tools=[get_weather, web_search, calculate_distance],  # Add here
    system_prompt="..."
)
```

### 2. Customize Agent Behavior

**System prompt in `01agent_basic_frontend.py`:**

```python
agent = create_agent(
    model=model,
    tools=[get_weather, web_search],
    system_prompt="""You are a specialized weather assistant.
    - Always provide weather in Celsius and Fahrenheit
    - Include UV index when possible
    - Warn about extreme weather
    - Be concise but informative"""
)
```

### 3. Add Custom Components (Generative UI)

**In `agent_generative_ui_backend.py`:**

```python
COMPONENT_CATALOG["components"]["WeatherCard"] = {
    "description": "Display weather with temperature and condition",
    "props": {
        "city": "string",
        "temperature": "number",
        "condition": "string",
        "icon": "string"
    }
}
```

### 4. Connect to Database

```python
def save_user_feedback(feedback: str) -> str:
    """Save user feedback to database"""
    # Save to database
    return "Feedback saved successfully"

# Add to agent tools
```

## 🔍 API Endpoints Reference

### Basic Agent API (`http://localhost:8000`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check if API is running |
| `/chat` | POST | Chat with agent |
| `/docs` | GET | Interactive API documentation |
| `/` | GET | API info |

**Chat Request:**
```json
{
  "message": "Your question here",
  "thread_id": "optional-conversation-id"
}
```

### Generative UI API (`http://localhost:8000`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check if API is running |
| `/catalog` | GET | Get available UI components |
| `/generate-ui` | POST | Generate UI spec |
| `/stream-ui` | POST | Stream UI spec (SSE) |
| `/agent/chat` | POST | Chat with UI-aware agent |

## 💻 React Integration Example

```typescript
import AgentGenerativeUI from './components/AgentGenerativeUI';

export default function App() {
  return (
    <div className="app">
      <header>
        <h1>🎨 AI UI Generator</h1>
      </header>
      <main>
        <AgentGenerativeUI />
      </main>
    </div>
  );
}
```

## 🧪 Testing Examples

### Test 1: Weather Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What'\''s the weather in London?"}'
```

### Test 2: Web Search
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for Python best practices"}'
```

### Test 3: Multi-turn Conversation
```bash
# Message 1
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What'\''s the weather in Paris?",
    "thread_id": "user-123"
  }'

# Message 2 (same conversation)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How about in Berlin?",
    "thread_id": "user-123"
  }'
```

The agent remembers previous messages in the same thread!

## 📈 Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│           React Frontend                        │
│  (Browser - Port 3000/5173)                    │
│  - User chat interface                         │
│  - UI spec rendering                           │
│  - Real-time updates                           │
└──────────────────────┬──────────────────────────┘
                       │ HTTPS
                       │
    ┌──────────────────┴──────────────────┐
    │                                     │
    ▼                                     ▼
┌──────────────────┐          ┌──────────────────────┐
│ Basic Agent API  │          │ Generative UI API    │
│ (Port 8000)      │          │ (Port 8000)          │
│ - Text responses │          │ - JSON UI specs      │
│ - Tools:         │          │ - Component catalog  │
│  • get_weather   │          │ - Streaming          │
│  • web_search    │          │ - Advanced agent     │
└──────────────────┘          └──────────────────────┘
         │                              │
         └──────────────┬───────────────┘
                        │
                        ▼
            ┌──────────────────────┐
            │  LangChain Agent     │
            │  (LLM + Tools)       │
            └──────────────────────┘
                        │
                        ▼
            ┌──────────────────────┐
            │  External Services   │
            │  - Weather API       │
            │  - Search API        │
            │  - Databases         │
            └──────────────────────┘
```

## 🎓 Learning Path

### Beginner
1. Start with basic agent API
2. Test chat endpoint
3. Understand how tools work
4. Build simple React chat UI

### Intermediate
1. Add custom tools
2. Implement conversation history
3. Add error handling
4. Deploy to production

### Advanced
1. Use Generative UI backend
2. Create custom UI components
3. Implement streaming
4. Build complex agent workflows

## 🚀 Deployment

### Local Development
```bash
# Terminal 1
python 01agent_basic_frontend.py

# Terminal 2
npm run dev  # React dev server
```

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY frontend/ .
CMD ["python", "01agent_basic_frontend.py"]
```

### Production Deployment
1. Use Gunicorn or similar for Python
2. Use nginx for reverse proxy
3. Enable HTTPS/SSL
4. Add authentication
5. Rate limiting
6. Error logging and monitoring

## 🔐 Security Considerations

1. **Input Validation** - Always validate user inputs
2. **Rate Limiting** - Prevent abuse
3. **Authentication** - Add user authentication
4. **CORS** - Restrict to trusted origins
5. **Error Handling** - Don't leak sensitive info
6. **Tool Permissions** - Control what tools agents can use

## 🐛 Troubleshooting

### Issue: "Connection refused on localhost:8000"
- Make sure Python backend is running
- Check firewall settings
- Try accessing http://localhost:8000/health

### Issue: "CORS error in browser"
- Backend CORS is already enabled in the code
- Check browser console for actual error

### Issue: "Agent responds with gibberish"
- Improve the system prompt
- Add more specific tool descriptions
- Check if model is working (try basic query)

### Issue: "Slow responses"
- Use a faster model (qwen3.5 vs gemma4)
- Optimize system prompt
- Check network latency

## 📚 Next Steps

1. **Explore the code** - Read through the comments in Python files
2. **Run examples** - Try different queries
3. **Build UI** - Create React components for your use case
4. **Add tools** - Integrate with your APIs/databases
5. **Deploy** - Get it running in production

## 🎉 You're Ready!

You have everything you need to build AI-powered applications with Generative UI. Start small, test thoroughly, and scale up.

**Questions?** Check:
- `/docs` endpoints for API info
- `GENERATIVE_UI_GUIDE.md` for concepts
- Code comments for implementation details

Happy building! 🚀✨
