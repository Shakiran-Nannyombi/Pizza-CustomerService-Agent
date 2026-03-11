"""
Session state management for Streamlit app
"""

import sys
from pathlib import Path
import streamlit as st

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pizza_agent.agents.api_agent import APIAgent
from pizza_agent.config import validate_config


def initialize_session_state():
    """Initialize all session state variables"""
    
    # Initialize chat messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Initialize agent
    if 'agent' not in st.session_state:
        try:
            if validate_config():
                st.session_state.agent = APIAgent(verbose=True)
                st.session_state.ai_mode = True
            else:
                st.session_state.agent = None
                st.session_state.ai_mode = False
        except Exception as e:
            st.session_state.agent = None
            st.session_state.ai_mode = False
            st.session_state.error_message = str(e)
    
    # Initialize other state vars
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0


def reset_conversation():
    """Clear chat history and reset agent"""
    st.session_state.messages = []
    if st.session_state.agent:
        st.session_state.agent.reset_conversation()
    st.session_state.conversation_count = 0


def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.messages.append({
        "role": role,
        "content": content
    })
    st.session_state.conversation_count += 1


def get_messages():
    """Get all chat messages"""
    return st.session_state.messages


def is_ai_mode() -> bool:
    """Check if AI mode is active"""
    return st.session_state.get('ai_mode', False)


def get_agent():
    """Get the agent instance"""
    return st.session_state.get('agent', None)
