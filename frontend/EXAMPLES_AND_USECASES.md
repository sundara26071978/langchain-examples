# 🎨 Generative UI Examples & Use Cases

## Visual Examples

### Example 1: Login Form

**User Request:**
```
"Create a professional login form with email and password fields"
```

**Generated UI Spec:**
```json
{
  "root": "login-form",
  "elements": {
    "login-form": {
      "type": "Card",
      "props": { "title": "Sign In", "padding": "lg" },
      "children": ["form-content"]
    },
    "form-content": {
      "type": "Stack",
      "props": { "direction": "vertical", "gap": "md" },
      "children": ["email-field", "password-field", "submit-btn", "forgot-link"]
    },
    "email-field": {
      "type": "TextInput",
      "props": { 
        "label": "Email Address",
        "placeholder": "you@example.com",
        "type": "email"
      },
      "children": []
    },
    "password-field": {
      "type": "TextInput",
      "props": {
        "label": "Password",
        "placeholder": "••••••••",
        "type": "password"
      },
      "children": []
    },
    "submit-btn": {
      "type": "Button",
      "props": { "label": "Sign In", "variant": "primary", "fullWidth": true },
      "children": []
    },
    "forgot-link": {
      "type": "Text",
      "props": { "content": "Forgot password?", "size": "sm" },
      "children": []
    }
  }
}
```

**Rendered UI:**
```
┌─────────────────────────────────┐
│         Sign In                 │
├─────────────────────────────────┤
│ Email Address                   │
│ [you@example.com............]   │
│                                 │
│ Password                        │
│ [••••••••........................]│
│                                 │
│ [     Sign In     ]             │
│ Forgot password?                │
└─────────────────────────────────┘
```

### Example 2: Weather Dashboard

**User Request:**
```
"Create a weather dashboard showing current temperature, conditions, and hourly forecast"
```

**Generated Structure:**
```
┌──────────────────────────────────────┐
│  Weather Dashboard - New York        │
├──────────────────────────────────────┤
│ ┌────────────────┐ ┌──────────────┐ │
│ │ Current:       │ │ ☀️ Sunny      │ │
│ │ 72°F           │ │ Feels: 70°F  │ │
│ │ Humidity: 65%  │ │ Wind: 5 mph  │ │
│ └────────────────┘ └──────────────┘ │
│                                      │
│ Hourly Forecast:                     │
│ ┌──┬──┬──┬──┬──┬──┬──┬──┐           │
│ │10│11│12│ 1│ 2│ 3│ 4│ 5│ AM       │
│ │73│74│75│76│75│74│72│71│°F       │
│ │☀️│☀️│⛅│⛅│🌤️│🌤️│⛅│☁️│         │
│ └──┴──┴──┴──┴──┴──┴──┴──┘           │
└──────────────────────────────────────┘
```

### Example 3: Feedback Form

**User Request:**
```
"Build a customer feedback form with rating, comments, and email field"
```

**Generated UI:**
```
┌────────────────────────────────────┐
│ Customer Feedback                  │
├────────────────────────────────────┤
│ Email                              │
│ [.................................]│
│                                    │
│ How would you rate our service?    │
│ ⭐ ⭐ ⭐ ⭐ ⭐                        │
│                                    │
│ Comments                           │
│ [...............................] │
│ [...............................] │
│ [...............................] │
│                                    │
│ [  Submit Feedback  ]              │
└────────────────────────────────────┘
```

## Real-World Use Cases

### 1. E-Commerce Product Filter

**Scenario:** User wants to filter products by price, category, and rating

```python
# Backend code
user_input = "Create a product filter for my online store"

# Agent generates:
{
  "type": "Card",
  "children": [
    {"type": "TextInput", "props": {"label": "Price Range"}},
    {"type": "Select", "props": {"label": "Category"}},
    {"type": "Slider", "props": {"label": "Min Rating"}},
    {"type": "Button", "props": {"label": "Apply Filters"}}
  ]
}

# Frontend renders: Interactive filter UI
```

### 2. API Response Formatter

**Scenario:** API returns complex data, agent formats as UI

```python
# API returns weather data:
{
  "temp": 72,
  "condition": "sunny",
  "humidity": 65,
  "wind": 5
}

# Agent generates UI to display it:
{
  "type": "Card",
  "children": [
    {"type": "Badge", "props": {"label": "☀️ Sunny", "variant": "success"}},
    {"type": "Text", "props": {"content": "72°F"}},
    {"type": "Stack", "children": [
      {"type": "Text", "props": {"content": "Humidity: 65%"}},
      {"type": "Text", "props": {"content": "Wind: 5 mph"}}
    ]}
  ]
}
```

### 3. Dynamic Form Based on User Type

```python
# User prompt: "Create a signup form"

# Backend knows user context:
if user_type == "business":
    # Generate: Company field, employee count, etc.
    form_spec = {...company_fields...}
elif user_type == "individual":
    # Generate: Name, email, password
    form_spec = {...simple_fields...}

# Frontend renders appropriate form
```

### 4. Data Visualization

**Scenario:** Convert data to visual representation

```python
# Data provided:
sales_data = [
  {"month": "Jan", "sales": 1000},
  {"month": "Feb", "sales": 1500},
  {"month": "Mar", "sales": 1200},
]

# Agent generates chart UI:
{
  "type": "Card",
  "props": {"title": "Sales Report"},
  "children": [
    {
      "type": "Chart",
      "props": {
        "data": sales_data,
        "type": "line",
        "xAxis": "month",
        "yAxis": "sales"
      }
    }
  ]
}
```

## Workflow Examples

### Workflow 1: Multi-Step Form

```
Step 1: User asks for "step-by-step signup form"
        Agent generates: Step indicator + Current form + Next button

Step 2: User fills form and clicks Next
        Agent generates: Next step form

Step 3: User completes all steps
        Agent generates: Success message
```

### Workflow 2: Search and Filter

```
Step 1: User enters search query
        Agent generates: Search form + Empty results

Step 2: Results return
        Agent generates: Filter panel + Result cards

Step 3: User applies filters
        Agent regenerates: Filtered results
```

### Workflow 3: Conditional Display

```
Step 1: User sees initial form
        Agent generates: Basic fields

Step 2: User selects "Other" category
        Agent regenerates: Additional fields for "Other"

Step 3: User's choice updates UI dynamically
```

## Code Examples

### Backend: Generate UI for User Preferences

```python
@app.post("/generate/user-form")
async def generate_user_form(request: dict):
    """Generate appropriate form based on user type"""
    
    user_type = request.get("user_type")  # "business" or "individual"
    
    # Prompt agent to generate appropriate form
    message = f"Create a {user_type} signup form"
    
    # Agent generates JSON spec
    spec = agent.generate_ui_spec(message)
    
    return spec.model_dump()
```

### Frontend: Render with Context

```typescript
const UserSignup = () => {
  const [userType, setUserType] = useState('individual');
  const [formSpec, setFormSpec] = useState(null);

  const handleUserTypeChange = async (type: string) => {
    setUserType(type);
    
    // Generate new form based on user type
    const response = await fetch('/generate/user-form', {
      method: 'POST',
      body: JSON.stringify({ user_type: type })
    });
    
    const spec = await response.json();
    setFormSpec(spec);
  };

  return (
    <>
      <RadioGroup value={userType} onChange={handleUserTypeChange}>
        <Radio value="individual">Individual</Radio>
        <Radio value="business">Business</Radio>
      </RadioGroup>
      
      {formSpec && <UIRenderer spec={formSpec} />}
    </>
  );
};
```

## Advanced Patterns

### Pattern 1: Adaptive UI

```python
def generate_adaptive_ui(context: dict):
    """Generate UI based on device, user preferences, etc."""
    
    device = context.get("device")  # "mobile", "tablet", "desktop"
    
    if device == "mobile":
        # Generate compact mobile-friendly UI
        return generate_mobile_spec()
    elif device == "desktop":
        # Generate full-featured desktop UI
        return generate_desktop_spec()
```

### Pattern 2: Progressive Disclosure

```python
def generate_progressive_form(step: int):
    """Show form fields progressively"""
    
    if step == 1:
        return {
            "elements": {
                "name": TextInput(...),
                "email": TextInput(...),
                "next": Button(...)
            }
        }
    elif step == 2:
        return {
            "elements": {
                "company": TextInput(...),
                "role": Select(...),
                "next": Button(...),
                "back": Button(...)
            }
        }
```

### Pattern 3: Conditional Fields

```python
def generate_conditional_form(responses: dict):
    """Show/hide fields based on previous answers"""
    
    # User selected "Other" for industry
    if responses.get("industry") == "other":
        # Include custom industry field
        add_field("custom_industry", TextInput(...))
    
    # User marked as business
    if responses.get("type") == "business":
        # Include business-specific fields
        add_fields([
            "company_name",
            "employee_count",
            "industry"
        ])
```

## Performance Considerations

### Optimization 1: Lazy Component Loading

```typescript
const Component = lazy(() => import('./HeavyComponent'));

const spec = {
  "type": "Card",
  "children": [
    {"type": "LazyComponent", "props": {"loader": Component}}
  ]
};
```

### Optimization 2: Spec Caching

```python
# Cache frequently generated specs
@lru_cache(maxsize=100)
def generate_ui_spec(description: str):
    return agent.generate_spec(description)
```

### Optimization 3: Streaming Large Specs

```typescript
// Stream spec progressively
const stream = await fetch('/stream-ui', {
  method: 'POST',
  body: JSON.stringify({ description })
});

for await (const chunk of stream) {
  // Add UI elements as they arrive
  addElement(chunk.element);
}
```

## Troubleshooting Guide

### Issue: Agent generates invalid components

**Solution:** Improve catalog descriptions
```python
"Card": {
    "description": "A bordered container with shadow, used for grouping related content. Props: title (optional), padding (sm/md/lg)",
    "props": {...}
}
```

### Issue: UI is too complex

**Solution:** Use progressive rendering
```typescript
<Renderer spec={spec} loading={isLoading} />
// loading={true} skips incomplete elements
```

### Issue: Slow generation

**Solution:** Use faster model or streaming
```python
# Use faster model
model = ChatOllama(model="qwen3.5:latest")

# Or use streaming
for chunk in agent.stream(message):
    yield chunk
```

## Summary

Generative UI enables:
- ✅ Dynamic form generation
- ✅ Responsive interfaces
- ✅ Real-time UI updates
- ✅ AI-powered UX
- ✅ Scalable to any complexity

Start with simple examples and gradually add complexity!
