"""
Chat interface component for Pizza Customer Service Agent
Handles chat display, user input, and message rendering
"""

import streamlit as st
from utils.session import add_message, get_messages, get_agent


def render_welcome_message():
    """Display welcome message when chat is empty"""
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h2>Welcome to Pizza Customer Service!</h2>
        <p style='font-size: 1.1em; color: #666; margin-top: 20px;'>
            I'm here to help you with:
        </p>
        <div style='margin-top: 30px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;'>
            <ul style='font-size: 1em; line-height: 2;'>
                <li>Pizza recommendations and menu information</li>
                <li>Order calculations and pricing</li>
                <li>Store hours and locations</li>
                <li>Delivery availability and estimates</li>
                <li>Current deals and promotions</li>
            </ul>
        </div>
        <p style='margin-top: 30px; color: #888;'>
            Type your question below to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    """Render a single chat message"""
    if role == "user":
        st.markdown(f"""
        <div class='chat-message user-message'>
            <div class='message-content'>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='chat-message assistant-message'>
            <div class='message-content'>{content}</div>
        </div>
        """, unsafe_allow_html=True)


def fallback_response(user_input: str) -> str:
    """Generate fallback response when AI is unavailable"""
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ['menu', 'pizza', 'topping', 'size']):
        return "I'd love to help with our menu! We offer various sizes and toppings. Please check our menu for details."
    elif any(word in user_lower for word in ['hour', 'open', 'close', 'time']):
        return "Our stores are typically open from 11 AM to 11 PM. Hours may vary by location."
    elif any(word in user_lower for word in ['delivery', 'deliver']):
        return "We offer delivery within a certain radius of our stores. Delivery times are typically 30-45 minutes."
    elif any(word in user_lower for word in ['location', 'where', 'address']):
        return "We have multiple locations. Please provide your address to find the nearest store."
    elif any(word in user_lower for word in ['price', 'cost', 'how much']):
        return "Prices vary by size and toppings. A medium pizza starts around $12."
    else:
        return "Thank you for your message. How can I help you with your pizza order today?"


def render_chat_interface():
    """Render the main chat interface"""
    
    # Display chat messages
    messages = get_messages()
    for message in messages:
        render_chat_message(message["role"], message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        add_message("user", prompt)
        render_chat_message("user", prompt)
        
        # Get agent response
        agent = get_agent()
        if agent:
            try:
                with st.spinner("Thinking..."):
                    response = agent.chat(prompt)
                add_message("assistant", response)
                render_chat_message("assistant", response)
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                add_message("assistant", error_msg)
                render_chat_message("assistant", error_msg)
        else:
            # Fallback mode
            response = fallback_response(prompt)
            add_message("assistant", response)
            render_chat_message("assistant", response)
        
        # Rerun to update the UI
        st.rerun()
