# Modular Architecture Guide

## Overview

The Pizza Customer Service Agent is now built with a clean modular architecture:

- **Frontend**: Streamlit UI with component-based design
- **Backend**: FastAPI REST API for AI agent interactions
- **Core**: Pizza agent package with tools and configuration

## Architecture Diagram

```bash
Pizza-CustomerService-Agent/
│
├── streamlit/                     # Frontend UI Layer
│   ├── app.py                     # Main Streamlit application
│   ├── components/                # Reusable UI components
│   │   ├── chat_interface.py      # Chat display and input
│   │   └── sidebar.py             # Sidebar with quick actions
│   └── utils/                     # Frontend utilities
│       ├── styling.py             # Custom CSS styling
│       ├── session.py             # Session state management
│       └── api_client.py          # Backend API communication
│
├── api/                           # Backend API Layer
│   ├── main.py                    # FastAPI application
│   └── models.py                  # Pydantic request/response models
│
├── pizza_agent/                   # Core Business Logic
│   ├── agents/
│   │   └── api_agent.py           # AI agent with Groq
│   ├── tools/
│   │   └── pizza_tools.py         # 8 pizza ordering tools
│   ├── knowledge/                 # Knowledge base documents
│   │   ├── pizza_menu.md
│   │   ├── store_locations.md
│   │   └── policies_faq.md
│   └── config.py                  # Configuration management
│
└── docs/                          # Documentation
    ├── README.md                  # Full documentation
    ├── ARCHITECTURE.md            # This file
    └── QUICKSTART.md              # Quick start guide
```

## Request Flow

```bash
User Input (Streamlit)
    ↓
components/chat_interface.py
    ↓
utils/api_client.py (HTTP POST)
    ↓
FastAPI (api/main.py) - /chat endpoint
    ↓
pizza_agent.agents.api_agent.APIAgent
    ↓
pizza_agent.tools (execute tools as needed)
    ↓
Response flows back through the stack
    ↓
Display in chat_interface.py
```

## Component Responsibilities

### Frontend (Streamlit)

**app.py**

- Main entry point
- Page configuration
- Component orchestration

**components/chat_interface.py**

- Chat message display
- User input handling
- Message rendering (user vs assistant)

**components/sidebar.py**

- Quick action buttons
- Status indicators
- Conversation controls

**utils/session.py**

- Session state initialization
- State management helpers
- Agent instance management

**utils/api_client.py**

- HTTP client for backend API
- Request/response handling
- Error handling and retries

**utils/styling.py**

- Custom CSS definitions
- Theme configuration
- Responsive styling

### Backend (FastAPI)

**api/main.py**

- FastAPI application setup
- CORS configuration
- Endpoint definitions:
  - `GET /` - Root/health check
  - `GET /status` - API status
  - `POST /chat` - Process chat messages
  - `POST /reset` - Reset conversation
  - `GET /tools` - List available tools

**api/models.py**

- Pydantic models for type safety
- Request validation
- Response schemas

### Core (Pizza Agent)

**pizza_agent/agents/api_agent.py**

- APIAgent class
- Groq API integration
- Tool orchestration
- Knowledge base loading

**pizza_agent/tools/pizza_tools.py**

- 8 specialized tools:
  1. get_pizza_quantity
  2. recommend_pizza
  3. check_store_hours
  4. find_nearest_location
  5. check_delivery_availability
  6. get_special_deals
  7. calculate_order_total
  8. get_estimated_delivery_time

**pizza_agent/config.py**

- Environment configuration
- Path management
- Config validation

## Running the Application

### Option 1: Launch All Services (Recommended)

```bash
python launch.py
```

This starts:

- FastAPI backend on <http://localhost:8000>
- Streamlit frontend on <http://localhost:8501>

### Option 2: Launch Separately

**Terminal 1 - Backend:**

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```bash
streamlit run frontend/streamlit/app.py
```

## Development

### Adding New Components

**Frontend Component:**

```python
# frontend/streamlit/components/my_component.py
import streamlit as st

def render_my_component():
    st.write("My new component")
```

**Import in app.py:**

```python
from components.my_component import render_my_component
```

### Adding New API Endpoints

**Add to api/main.py:**

```python
@app.get("/my-endpoint")
async def my_endpoint():
    return {"message": "Hello"}
```

**Add model to api/models.py:**

```python
class MyResponse(BaseModel):
    message: str
```

### Adding New Tools

Add to `pizza_agent/tools/pizza_tools.py`:

```python
def my_new_tool(param: str) -> str:
    """Tool description"""
    return f"Result for {param}"
```

Update tool registration in `api_agent.py`.

## Benefits of This Architecture

1. **Separation of Concerns**: UI, API, and business logic are distinct
2. **Maintainability**: Small, focused files instead of monolithic code
3. **Scalability**: Easy to add new components or endpoints
4. **Testing**: Each layer can be tested independently
5. **Reusability**: Components can be used across different pages
6. **Type Safety**: Pydantic models ensure data validation
7. **API First**: Backend can serve multiple frontends (web, mobile, etc.)

## Testing Individual Layers

**Test Backend API:**

```bash
# Using curl
curl http://localhost:8000/status
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Or visit http://localhost:8000/docs for interactive API docs
```

**Test Frontend Components:**

```bash
streamlit run frontend/streamlit/app.py
```

**Test Core Agent:**

```bash
python examples/demo.py
```

## Environment Variables

Create `.env` file in project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

## Dependencies

Install all dependencies:

```bash
pip install -r requirements.txt
```

Key packages:

- `streamlit` - Frontend UI framework
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `requests` - HTTP client for frontend
- `openai` - Groq API client (OpenAI-compatible)
- `pydantic` - Data validation

## Troubleshooting

**Backend won't start:**

- Check `.env` file exists with valid GROQ_API_KEY
- Verify port 8000 is available
- Run `python -m uvicorn api.main:app --reload` for debug mode

**Frontend can't connect to backend:**

- Ensure backend is running on <http://localhost:8000>
- Check console for connection errors
- Verify `api_client.py` has correct base_url

**Import errors:**

- Run from project root directory
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

1. Run the application: `python launch.py`
2. Open browser to <http://localhost:8501>
3. Start chatting with the pizza agent
4. Explore API docs at <http://localhost:8000/docs>

For more information, see the main [README.md](../README.md)
