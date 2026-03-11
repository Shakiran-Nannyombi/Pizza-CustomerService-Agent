# Pizza Customer Service Agent

AI-powered pizza ordering assistant built with Groq API and LLaMA 3.1.

## Project Structure

```bash
Pizza-CustomerService-Agent/
├── streamlit/          # Frontend UI (Streamlit)
├── pizza_agent/        # Core agent logic and tools
├── api/                # Backend API (FastAPI)
└── docs/               # Documentation
```

## Quick Start

### Prerequisites

- Python 3.12+
- Groq API key ([Get one free](https://console.groq.com))

### Installation

1. Clone the repository
2. Create virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:

   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

**Option 1: Docker (recommended for deployment)**

```bash
# Quick start with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:8501
# API: http://localhost:8000
```

See [Docker Deployment Guide](docs/DOCKER.md) for complete Docker deployment guide.

**Option 2: Launch everything locally**

```bash
python launch.py
```

This starts both backend (port 8000) and frontend (port 8501).

**Option 3: Launch separately**

Terminal 1 (Backend):

```bash
python -m uvicorn api.main:app --reload
```

Terminal 2 (Frontend):

```bash
streamlit run streamlit/app.py
```

## Access Points

- **Streamlit UI**: <http://localhost:8501>
- **FastAPI Backend**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>

## Features

- 8 specialized tools for pizza ordering
- Natural language understanding
- RAG-based knowledge retrieval
- Store information and hours
- Delivery availability checks
- Order calculations and recommendations
- Current deals and promotions

## Architecture

- **Frontend**: Streamlit with modular component design
- **Backend**: FastAPI REST API
- **AI**: Groq API with LLaMA 3.1 (70B)
- **Tools**: Custom pizza ordering functions

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Getting started
- [Architecture](docs/ARCHITECTURE.md) - System design and structure
- [Docker Deployment](docs/DOCKER.md) - Container deployment guide
- [Docker Quick Reference](docs/DOCKER-QUICKREF.md) - Docker commands cheat sheet

## Deployment

### Docker Deployment (Recommended)

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

See [Docker Deployment Guide](docs/DOCKER.md) for:
- Complete deployment guide
- Environment configuration
- Production setup with Nginx
- Scaling and monitoring
- Troubleshooting

### Manual Deployment

For non-Docker deployments, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

## Development

### Folder Structure

**streamlit/** - Frontend application

- `app.py` - Main Streamlit app
- `components/` - Reusable UI components
- `utils/` - Helper utilities

**pizza_agent/** - Core agent package

- `agents/` - API agent implementation
- `tools/` - Pizza ordering tools
- `knowledge/` - Knowledge base documents
- `config.py` - Configuration management

**api/** - Backend services

- `main.py` - FastAPI application
- `models.py` - Pydantic models

**docs/** - Documentation

- All project documentation and guides

### Adding New Features

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed development guide.

## License

See LICENSE file for details.

## Support

For issues or questions, please check the documentation in the `docs/` folder.

---

Built with Groq, LLaMA 3.1, FastAPI, and Streamlit.
