"""
Configuration settings for Pizza Agent
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
SRC_DIR = BASE_DIR / "src"

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.1-70b-versatile"

# Backwards compatibility
LLAMA_API_KEY = GROQ_API_KEY  # Use Groq key
LLAMA_API_URL = GROQ_API_URL
LLAMA_MODEL = GROQ_MODEL

# Agent Settings
MAX_CONVERSATION_HISTORY = 10
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 512

# Knowledge Base Files
KNOWLEDGE_FILES = {
    "menu": KNOWLEDGE_DIR / "pizza_menu.md",
    "locations": KNOWLEDGE_DIR / "store_locations.md",
    "policies": KNOWLEDGE_DIR / "policies_faq.md"
}

def get_knowledge_path(filename: str) -> Path:
    """Get full path to a knowledge base file"""
    return KNOWLEDGE_DIR / filename

def validate_config() -> bool:
    """Validate configuration"""
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not set in .env file")
        return False
    
    if not KNOWLEDGE_DIR.exists():
        print(f"Warning: Knowledge directory not found: {KNOWLEDGE_DIR}")
        return False
    
    return True
