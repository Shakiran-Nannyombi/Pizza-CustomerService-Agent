"""
AI-Powered Pizza Agent using LLaMA API
"""

from typing import Dict, List, Tuple, Optional
from openai import OpenAI

from pizza_agent.config import (
    LLAMA_API_KEY,
    LLAMA_API_URL,
    LLAMA_MODEL,
    MAX_CONVERSATION_HISTORY,
    DEFAULT_TEMPERATURE,
    MAX_TOKENS,
    KNOWLEDGE_DIR
)
from pizza_agent.tools import (
    get_pizza_quantity,
    recommend_pizza,
    check_store_hours,
    find_nearest_location,
    check_delivery_availability,
    get_special_deals,
    get_estimated_delivery_time,
    calculate_order_total,
    start_new_order,
    add_pizza_to_order,
    add_side_to_order,
    add_drink_to_order,
    review_current_order,
    add_special_instructions,
    confirm_order,
    cancel_current_order,
    get_order_status
)


class APIAgent:
    """AI-powered agent using LLaMA API"""
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize the API agent
        
        Args:
            api_key: LLaMA API key (uses config if not provided)
            verbose: Print debug information
        """
        self.api_key = api_key or LLAMA_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found! Set it in .env file or get one free at https://console.groq.com/")
        
        self.verbose = verbose
        
        # Initialize OpenAI client with LLaMA endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=LLAMA_API_URL
        )
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Conversation history
        self.messages: List[Dict[str, str]] = []
        
        if self.verbose:
            print(f"API Agent initialized")
            print(f"Knowledge base: {len(self.knowledge_base)} documents")
    
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load knowledge base documents"""
        kb = {}
        
        if not KNOWLEDGE_DIR.exists():
            print(f"Warning: Knowledge directory not found: {KNOWLEDGE_DIR}")
            return kb
        
        for doc_file in KNOWLEDGE_DIR.glob("*.md"):
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    kb[doc_file.stem] = f.read()
            except Exception as e:
                print(f"Warning: Could not load {doc_file.name}: {e}")
        
        return kb
    
    def _search_knowledge(self, query: str) -> str:
        """Search knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        for doc_name, content in self.knowledge_base.items():
            if any(word in content.lower() for word in query_lower.split()):
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if any(word in line.lower() for word in query_lower.split()):
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        results.append('\n'.join(lines[start:end]))
                        break
        
        return '\n\n'.join(results[:3]) if results else "No information found."
    
    def _detect_intent_and_execute(self, user_input: str) -> Tuple[Optional[str], Optional[str]]:
        """Detect user intent and execute appropriate tool"""
        user_lower = user_input.lower()
        
        # Order management - Start new order
        if any(phrase in user_lower for phrase in ['start order', 'place order', 'i want to order', 'order pizza', 'my name is']):
            # Try to extract name and phone
            if 'my name is' in user_lower:
                return ("order_prompt", "Great! To start your order, I'll need your phone number for the order.")
            return ("order_prompt", "I'd be happy to help you order! Can I get your name and phone number to start?")
        
        # Review order
        if any(phrase in user_lower for phrase in ['review order', 'check order', 'what do i have', 'order summary', 'my order']):
            result = review_current_order()
            if result['success']:
                order = result['order']
                summary = f"Here's your order:\n\n"
                for item in order['items']:
                    summary += f"- {item['quantity']}x {item['size']} {item['name']}"
                    if item['customizations']:
                        summary += f" ({item['customizations']})"
                    summary += f" - {item['price']}\n"
                summary += f"\nSubtotal: {order['subtotal']}\n"
                summary += f"Tax: {order['tax']}\n"
                summary += f"Delivery Fee: {order['delivery_fee']}\n"
                summary += f"Total: {order['total']}"
                return ("order_review", summary)
            return ("order_review", result['message'])
        
        # Confirm order
        if any(phrase in user_lower for phrase in ['confirm order', 'place the order', 'finalize order', "that's all", "that's it", 'complete order']):
            result = confirm_order()
            if result['success']:
                order = result['order']
                msg = f"✅ {result['message']}\n\nOrder #{order['order_id']}\n"
                msg += f"Total: {order['total']}\n"
                msg += f"Type: {order['order_type'].title()}\n"
                if order['order_type'] == 'delivery':
                    msg += f"Delivery to: {order['customer_address']}\n"
                msg += f"\nEstimated time: 30-45 minutes"
                return ("order_confirm", msg)
            return ("order_confirm", result['message'])
        
        # Cancel order
        if any(phrase in user_lower for phrase in ['cancel order', 'start over', 'clear order']):
            result = cancel_current_order()
            return ("order_cancel", result['message'])
        
        # Pizza quantity calculation
        if any(word in user_lower for word in ['how many', 'quantity', 'people', 'feed']):
            words = user_input.split()
            for word in words:
                if word.isdigit():
                    return ("quantity", get_pizza_quantity(int(word)))
        
        # Pizza recommendations
        if any(word in user_lower for word in ['recommend', 'suggest', 'what should', 'which pizza']):
            if any(word in user_lower for word in ['vegetarian', 'veggie', 'no meat']):
                return ("recommend", recommend_pizza('vegetarian'))
            elif any(word in user_lower for word in ['meat', 'protein']):
                return ("recommend", recommend_pizza('meat lover'))
            elif any(word in user_lower for word in ['spicy', 'hot']):
                return ("recommend", recommend_pizza('spicy'))
            else:
                return ("recommend", recommend_pizza('popular'))
        
        # Store hours
        if any(word in user_lower for word in ['hours', 'open', 'close', 'when']):
            for location in ['downtown', 'riverside', 'westside', 'eastend']:
                if location in user_lower:
                    return ("hours", check_store_hours(location))
            return ("hours", check_store_hours('downtown'))
        
        # Location search
        if any(word in user_lower for word in ['location', 'where', 'address', 'find store']):
            return ("location", find_nearest_location())
        
        # Delivery inquiries
        if any(word in user_lower for word in ['deliver', 'delivery']):
            if 'time' in user_lower or 'how long' in user_lower:
                return ("delivery_time", get_estimated_delivery_time())
            else:
                return ("delivery_info", check_delivery_availability("your address"))
        
        # Special deals
        if any(word in user_lower for word in ['deal', 'special', 'discount', 'promotion']):
            return ("deals", get_special_deals())
        
        # Menu information
        if any(word in user_lower for word in ['menu', 'what do you have', 'pizzas', 'price']):
            return ("menu", self._search_knowledge(user_input))
        
        return (None, None)
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and generate AI response
        
        Args:
            user_input: User's message
            
        Returns:
            Agent's response
        """
        try:
            # Try to handle with tools first
            intent, tool_result = self._detect_intent_and_execute(user_input)
            
            if intent and tool_result:
                # Use AI to make the tool result conversational
                system_msg = "You are a friendly Pizza Customer Service Agent. Respond naturally based on the information provided."
                prompt = f"Customer asked: {user_input}\n\nInfo: {tool_result}\n\nRespond naturally:"
                
                response = self.client.chat.completions.create(
                    model=LLAMA_MODEL,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=DEFAULT_TEMPERATURE,
                    max_tokens=MAX_TOKENS
                )
                
                return response.choices[0].message.content.strip()
            
            # No tool match - use AI with knowledge base
            system_msg = f"""You are a helpful Pizza Restaurant Customer Service Agent. Your job is to help customers order pizza, answer questions, and provide excellent service.

IMPORTANT ORDER-TAKING INSTRUCTIONS:
1. When a customer wants to order, ask for their name and phone number first
2. Ask if it's for delivery (need address) or pickup
3. Help them build their order by suggesting items from the menu
4. Confirm each item as you add it
5. Offer to review the order before finalizing
6. Be friendly, patient, and helpful

AVAILABLE ACTIONS:
- Start orders: Ask for name, phone, and address (if delivery)
- Add items: Pizzas, sides, drinks, desserts
- Review order: Show what they've ordered so far
- Confirm order: Finalize and submit the order
- Cancel order: Start over if needed

Knowledge Base:
{self._get_kb_summary()}

Answer questions about pizzas, menu, stores, delivery, and deals.
Be friendly, conversational, and help customers make great choices!"""
            
            # Add to conversation history
            self.messages.append({"role": "user", "content": user_input})
            
            # Keep conversation history limited
            if len(self.messages) > MAX_CONVERSATION_HISTORY:
                self.messages = self.messages[-MAX_CONVERSATION_HISTORY:]
            
            # Get AI response
            response = self.client.chat.completions.create(
                model=LLAMA_MODEL,
                messages=[
                    {"role": "system", "content": system_msg},
                    *self.messages
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            
            assistant_msg = response.choices[0].message.content.strip()
            self.messages.append({"role": "assistant", "content": assistant_msg})
            
            return assistant_msg
            
        except Exception as e:
            error_str = str(e)
            if "api" in error_str.lower() or "auth" in error_str.lower():
                return f"API Error: {error_str}\n\nPlease check your GROQ_API_KEY. Get one free at: https://console.groq.com/"
            return f"Sorry, I encountered an error: {error_str}"
    
    def _get_kb_summary(self) -> str:
        """Get summary of knowledge base"""
        summaries = []
        for name, content in self.knowledge_base.items():
            summary = content[:200] + "..." if len(content) > 200 else content
            summaries.append(f"=== {name} ===\n{summary}")
        return "\n\n".join(summaries)
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.messages = []
