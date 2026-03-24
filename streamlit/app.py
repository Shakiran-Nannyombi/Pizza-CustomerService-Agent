"""
Main Streamlit Application - Pizza Customer Service Agent
Modular architecture with component-based design
"""

import streamlit as st
from utils.styling import get_custom_css
from utils.session import (
    initialize_session_state,
    reset_conversation,
    add_message,
    get_messages,
    is_ai_mode,
    get_agent
)
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, render_welcome_message


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="Pizza Customer Service Agent",
        page_icon="🍕",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown(
        "<h1 class='main-header'>Pizza Customer Service Agent</h1>",
        unsafe_allow_html=True
    )
    
    # Flying Stickers for Streamlit
    st.markdown("""
        <style>
            @keyframes float {
                0% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(10deg); }
                100% { transform: translateY(0px) rotate(0deg); }
            }
            .st-sticker {
                position: fixed;
                font-size: 3rem;
                animation: float 4s ease-in-out infinite;
                z-index: 100;
                pointer-events: none;
                opacity: 0.6;
            }
        </style>
        <div class="st-sticker" style="top: 10%; left: 5%; animation-delay: 0s;">🍕</div>
        <div class="st-sticker" style="top: 20%; right: 10%; animation-delay: 1s;">🌿</div>
        <div class="st-sticker" style="bottom: 15%; left: 15%; animation-delay: 2s;">🌶️</div>
        <div class="st-sticker" style="bottom: 10%; right: 20%; animation-delay: 1.5s;">🍄</div>
    """, unsafe_allow_html=True)
    
    # Check AI mode
    if not is_ai_mode():
        st.error(
            "Configuration error. Please check your .env file and ensure "
            "GROQ_API_KEY is set correctly."
        )
        if 'error_message' in st.session_state:
            st.error(f"Error details: {st.session_state.error_message}")
        return
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Show welcome message if no conversation yet
        if len(get_messages()) == 0:
            render_welcome_message()
        
        # Render chat interface
        render_chat_interface()


if __name__ == "__main__":
    main()
