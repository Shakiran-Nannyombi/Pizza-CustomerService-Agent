"""
Sidebar component for Pizza Customer Service Agent
Displays status, quick actions, and conversation controls
"""

import streamlit as st
from utils.session import reset_conversation, is_ai_mode, get_messages


def render_sidebar():
    """Render the sidebar with controls and status"""
    
    with st.sidebar:
        st.markdown("### Status")
        
        # AI Mode Status
        if is_ai_mode():
            st.success("AI Mode: Active")
            st.caption("Using Groq API (LLaMA 3.1)")
        else:
            st.warning("AI Mode: Fallback")
            st.caption("Using basic responses")
        
        # Conversation Stats
        st.markdown("---")
        st.markdown("### Conversation")
        message_count = len(get_messages())
        st.metric("Messages", message_count)
        
        # Quick Actions
        st.markdown("---")
        st.markdown("### Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Chat", use_container_width=True):
                reset_conversation()
                st.rerun()
        
        with col2:
            if st.button("Refresh", use_container_width=True):
                st.rerun()
        
        # Suggested Prompts
        st.markdown("---")
        st.markdown("### Try asking:")
        
        suggestions = [
            "Show me your menu",
            "What deals do you have?",
            "I need pizza for 15 people",
            "Do you deliver to my area?",
            "What are your store hours?"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"suggestion_{suggestion}", use_container_width=True):
                st.session_state.suggested_prompt = suggestion
                st.rerun()
        
        # Info Section
        st.markdown("---")
        st.markdown("### About")
        st.caption("Pizza Customer Service Agent v1.0")
        st.caption("Powered by Groq & LLaMA 3.1")
        
        # Links
        st.markdown("---")
        st.markdown("### Resources")
        st.markdown("[Documentation](../docs/README.md)")
        st.markdown("[Architecture](../docs/ARCHITECTURE.md)")
        st.markdown("[Quick Start](../docs/QUICKSTART.md)")
