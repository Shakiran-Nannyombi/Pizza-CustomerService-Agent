"""
Pizza Customer Service Agent - Gradio Web Interface

Beautiful chat interface for ordering pizzas with AI assistance.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

import gradio as gr
from pizza_agent.agents.api_agent import APIAgent
from pizza_agent.config import validate_config
from pizza_agent import (
    get_pizza_quantity,
    recommend_pizza,
    check_store_hours,
    find_nearest_location,
    get_special_deals
)


# Initialize the agent
try:
    if not validate_config():
        print("Warning: Configuration incomplete. Some features may not work.")
    
    agent = APIAgent(verbose=True)
    print("Agent ready!")
except Exception as e:
    print(f"Warning: Could not initialize AI agent: {e}")
    print("Running in demo mode with tools only...")
    agent = None


def chat_interface(message: str, history: list) -> str:
    """
    Process chat messages
    
    Args:
        message: User's message
        history: Chat history (list of [user, bot] pairs)
        
    Returns:
        Bot's response
    """
    if not message.strip():
        return "Please enter a message!"
    
    try:
        if agent:
            # Use AI agent
            response = agent.chat(message)
        else:
            # Fallback to rule-based responses
            response = _fallback_response(message)
        
        return response
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}\nPlease try again."


def _fallback_response(message: str) -> str:
    """Fallback responses using tools only"""
    msg_lower = message.lower()
    
    if any(word in msg_lower for word in ['menu', 'what do you have']):
        return """Our delicious pizzas include:
        
- Margherita ($12.99)
- Pepperoni ($14.99) 
- Meat Lovers ($18.99)
- Veggie Deluxe ($15.99)
- Supreme ($17.99)

What would you like to order?"""
    
    elif any(word in msg_lower for word in ['deal', 'special', 'discount']):
        return get_special_deals()
    
    elif any(word in msg_lower for word in ['location', 'where', 'address']):
        return find_nearest_location()
    
    elif any(word in msg_lower for word in ['hours', 'open', 'close']):
        return check_store_hours('downtown')
    
    elif any(word in msg_lower for word in ['recommend', 'suggest']):
        if 'vegetarian' in msg_lower or 'veggie' in msg_lower:
            return recommend_pizza('vegetarian')
        elif 'meat' in msg_lower:
            return recommend_pizza('meat lover')
        else:
            return recommend_pizza('popular')
    
    else:
        return "I can help you with menu items, special deals, store locations, hours, and recommendations. What would you like to know?"


def quick_action(action: str) -> str:
    """Handle quick action buttons"""
    actions = {
        "View Menu": "Show me your menu",
        "Special Deals": "What are the current deals?",
        "Store Locations": "Where are your stores?",
        "Store Hours": "What are your store hours?",
        "Vegetarian Options": "Recommend vegetarian pizzas"
    }
    return actions.get(action, "")


# Custom CSS for better appearance
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.chat-message {
    padding: 10px;
    border-radius: 8px;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="Pizza Order Agent", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown(
        """
        # Pizza Customer Service Agent
        ### AI-Powered Pizza Ordering Assistant
        
        Ask me anything about our menu, deals, locations, or let me help you order!
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            # Main chat interface
            chatbot = gr.Chatbot(
                label="Chat with Pizza Agent",
                height=500,
                bubble_full_width=False,
                avatar_images=(None, None),
                show_label=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Your Message",
                    placeholder="Type your message here... (e.g., 'Show me the menu' or 'I need pizza for 20 people')",
                    scale=4,
                    autofocus=True
                )
                submit = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                clear = gr.Button("Clear Chat")
        
        with gr.Column(scale=1):
            gr.Markdown("### Quick Actions")
            
            quick_buttons = [
                gr.Button("View Menu", size="sm"),
                gr.Button("Special Deals", size="sm"),
                gr.Button("Store Locations", size="sm"),
                gr.Button("Store Hours", size="sm"),
                gr.Button("Vegetarian Options", size="sm")
            ]
            
            gr.Markdown("### Features")
            gr.Markdown(
                """
                - AI-powered conversations
                - Menu recommendations
                - Order calculations  
                - Delivery information
                - Special deals & promotions
                - Store locations & hours
                """
            )
    
    gr.Markdown(
        """
        ---
        **Tip:** Try asking "I need pizzas for 15 people" or "What vegetarian options do you have?"
        """
    )
    
    # Event handlers
    def respond(message, chat_history):
        """Handle user message and update chat"""
        bot_message = chat_interface(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    def handle_quick_action(button_text, chat_history):
        """Handle quick action button clicks"""
        # Extract action text (remove emoji)
        action = button_text.split(" ", 1)[-1]
        user_message = quick_action(action)
        if user_message:
            bot_message = chat_interface(user_message, chat_history)
            chat_history.append((user_message, bot_message))
        return chat_history
    
    # Connect events
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)
    
    # Quick button handlers  
    for btn in quick_buttons:
        btn.click(
            handle_quick_action,
            inputs=[gr.State(btn.value), chatbot],
            outputs=[chatbot]
        )


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Pizza Customer Service Agent...")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
