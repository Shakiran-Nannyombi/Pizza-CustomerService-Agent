# Quick Start Guide

## Starting the Pizza Customer Service Agent

### Method 1: Launch Everything at Once (Recommended)

```bash
# Make sure you're in the project root
cd /home/dev-kiran/Desktop/Projects/Pizza-CustomerService-Agent

# Activate virtual environment
source .venv/bin/activate

# Run the launch script
python launch.py
```

This will start:

- **Backend API** on <http://localhost:8000>
- **Frontend UI** on <http://localhost:8501>

Your browser should automatically open to the Streamlit interface.

### Method 2: Launch Backend and Frontend Separately

**Terminal 1 (Backend):**

```bash
cd /home/dev-kiran/Desktop/Projects/Pizza-CustomerService-Agent
source .venv/bin/activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**

```bash
cd /home/dev-kiran/Desktop/Projects/Pizza-CustomerService-Agent
source .venv/bin/activate
streamlit run frontend/streamlit/app.py
```

### Method 3: Direct Agent Mode (No UI)

If you want to test the agent directly without the UI:

```bash
cd /home/dev-kiran/Desktop/Projects/Pizza-CustomerService-Agent
source .venv/bin/activate
python examples/demo.py
```

## Accessing the Application

Once running:

- **Streamlit UI**: <http://localhost:8501>
- **FastAPI Backend**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs> (Interactive Swagger UI)
- **Alternative API Docs**: <http://localhost:8000/redoc>

## Testing the API

### Using curl

```bash
# Check status
curl http://localhost:8000/status

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need 3 large pizzas"}'

# Get available tools
curl http://localhost:8000/tools

# Reset conversation
curl -X POST http://localhost:8000/reset
```

### Using the Interactive API Docs

1. Go to <http://localhost:8000/docs>
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Enter your parameters
5. Click "Execute"

## Stopping the Application

If you used `launch.py`:

- Press `Ctrl+C` in the terminal
- Both services will shutdown gracefully

If you launched separately:

- Press `Ctrl+C` in each terminal window

## Project Structure

```bash
Pizza-CustomerService-Agent/
├── launch.py              # All-in-one launcher
├── streamlit/             # Streamlit UI
│   ├── app.py            # Main UI app
│   ├── components/       # UI components
│   │   ├── chat_interface.py
│   │   └── sidebar.py
│   └── utils/            # UI utilities
│       ├── styling.py
│       ├── session.py
│       └── api_client.py
├── api/                   # FastAPI backend
│   ├── main.py           # API server
│   └── models.py         # Request/response models
├── pizza_agent/          # Core agent logic
│   ├── agents/
│   ├── tools/
│   ├── knowledge/
│   └── config.py
└── docs/                  # Documentation
```

## Common Issues

### Port Already in Use

If you get "Address already in use" error:

```bash
# Find and kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 8501 (frontend)
lsof -ti:8501 | xargs kill -9
```

### Import Errors

Make sure you're running from the project root:

```bash
cd /home/dev-kiran/Desktop/Projects/Pizza-CustomerService-Agent
source .venv/bin/activate
```

### Missing Dependencies

```bash
pip install -r requirements.txt
```

### API Key Not Found

Make sure `.env` file exists with:

```bash
GROQ_API_KEY=your_key_here
```

## What to Try

1. **Simple Orders**: "I want to order 2 large pepperoni pizzas"
2. **Recommendations**: "What pizza would you recommend for someone who likes spicy food?"
3. **Store Info**: "What are your store hours?"
4. **Delivery Check**: "Can you deliver to 123 Main St?"
5. **Pricing**: "How much would 3 medium pizzas cost?"
6. **Complex Orders**: "I'm having a party with 20 people, what should I order?"

## Next Steps

- See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture
- See [README.md](README.md) for full documentation
- Explore the code in `pizza_agent/` to understand the agent
- Check out `streamlit/components/` to see modular UI design

Enjoy your Pizza Customer Service Agent!
