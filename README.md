# Pizza Customer Service Agent

AI-powered pizza ordering assistant with a beautiful Gradio web interface. Built for the Microsoft Innovation Challenge.

## Features

- **AI-Powered Conversations** - Natural language understanding using Groq API (fast LLaMA inference)
- **Smart Recommendations** - Get pizza suggestions based on preferences
- **Order Calculations** - Calculate quantities for groups
- **Delivery Information** - Check delivery availability and times
- **Special Deals** - View current promotions and discounts
- **Store Locations** - Find nearby stores and hours
- **Beautiful UI** - Modern Gradio web interface

## Project Structure

```
Pizza-CustomerService-Agent/
├── app.py                      # Main Gradio web interface
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── .env                        # Your API keys (gitignored)
│
├── src/pizza_agent/           # Main package
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── agents/                # Agent implementations
│   │   ├── api_agent.py       # AI-powered agent
│   │   └── simple_agent.py    # Rule-based agent
│   └── tools/                 # Pizza ordering tools
│       └── pizza_tools.py
│
├── knowledge/                 # Knowledge base
│   ├── pizza_menu.md
│   ├── store_locations.md
│   └── policies_faq.md
│
├── examples/                  # Demo scripts
│   └── demo.py
│
└── docs/                      # Documentation
```

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo>
cd Pizza-CustomerService-Agent
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# or
.venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

Get your free Groq API key at: https://console.groq.com/

### 4. Launch the App

```bash
python app.py
# or
python main.py
```

The web interface will open at **http://localhost:7860**

## Usage

### Web Interface (Gradio)

The easiest way to use the agent:

```bash
python app.py
```

Features:
- Chat interface with message history
- Quick action buttons (Menu, Deals, Locations, etc.)
- Real-time AI responses
- Clean, modern UI

### Command Line

Run the demo:

```bash
python examples/demo.py --demo
```

### As a Python Package

```python
from pizza_agent.agents.api_agent import APIAgent

# Initialize agent
agent = APIAgent()

# Chat
response = agent.chat("I need pizzas for 20 people")
print(response)
```

## Development

### Project Components

**Agents** (`src/pizza_agent/agents/`)
- `api_agent.py` - AI-powered conversational agent using LLaMA API
- `simple_agent.py` - Rule-based fallback agent

**Tools** (`src/pizza_agent/tools/pizza_tools.py`)
- `get_pizza_quantity()` - Calculate pizzas needed
- `recommend_pizza()` - Suggest pizzas by preference
- `check_store_hours()` - Get store operating hours
- `find_nearest_location()` - Show all locations
- `check_delivery_availability()` - Check delivery zones
- `get_special_deals()` - Display current promotions
- `calculate_order_total()` - Calculate order costs
- `get_estimated_delivery_time()` - Estimate delivery

**Knowledge Base** (`knowledge/`)
- Menu items and pricing
- Store locations and hours
- Policies and FAQ

### Adding New Features

1. **Add a new tool:**
   - Add function to `src/pizza_agent/tools/pizza_tools.py`
   - Export in `__init__.py`
   - Update agent to use it

2. **Modify the UI:**
   - Edit `app.py`
   - Customize Gradio components
   - Add quick action buttons

3. **Update knowledge base:**
   - Add or edit markdown files in `knowledge/`
   - Agent will automatically load them

## Dependencies

- **openai** - LLaMA API client
- **gradio** - Web UI framework
- **python-dotenv** - Environment configuration
- **langchain** (optional) - Advanced agent features

## Configuration

Edit `src/pizza_agent/config.py`:

```python
LLAMA_MODEL = "llama3.1-70b"  # Change model
MAX_TOKENS = 512               # Response length
DEFAULT_TEMPERATURE = 0.7      # Creativity level
```

## Testing

Run tool demos:

```bash
# Test all tools
python examples/demo.py --demo

# Check environment
python scripts/quickstart.py
```

## API Keys

### Groq API (Recommended - Fast & Free)

Get your key from: https://console.groq.com/

Groq provides:
- Fast LLaMA 3.1 inference
- Free tier with generous limits
- OpenAI-compatible API
- No credit card required

Update `src/pizza_agent/config.py` to use different models if needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

See [LICENSE](license.md) for details.

## Troubleshooting

**"GROQ_API_KEY not found"**
- Create `.env` file in project root
- Add: `GROQ_API_KEY=your_key`
- Get free key: https://console.groq.com/

**"Module not found"**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

**"Knowledge base not found"**
- Ensure `knowledge/` folder exists
- Add `.md` files with menu, locations, policies

**Gradio won't start**
- Check port 7860 is available
- Try different port in `app.py`

## Contact

For questions or issues, please open a GitHub issue.

---

**Built for the Microsoft Innovation Challenge**
