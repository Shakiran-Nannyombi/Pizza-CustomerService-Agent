"""
Order Management System for Pizza Restaurant
Handles order creation, tracking, and management
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import uuid


class Order:
    """Represents a pizza order"""
    
    def __init__(self, customer_name: str, customer_phone: str, customer_address: str = None):
        self.order_id = str(uuid.uuid4())[:8].upper()
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address
        self.items = []
        self.order_type = "delivery" if customer_address else "pickup"
        self.status = "pending"
        self.created_at = datetime.now()
        self.subtotal = 0.0
        self.tax = 0.0
        self.delivery_fee = 0.0
        self.total = 0.0
        self.special_instructions = ""
    
    def add_item(self, item_name: str, size: str, quantity: int, price: float, customizations: str = ""):
        """Add an item to the order"""
        self.items.append({
            "name": item_name,
            "size": size,
            "quantity": quantity,
            "price": price,
            "customizations": customizations
        })
        self._calculate_totals()
    
    def _calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item['price'] * item['quantity'] for item in self.items)
        
        # Calculate delivery fee
        if self.order_type == "delivery":
            if self.subtotal < 15:
                self.delivery_fee = 4.99
            elif self.subtotal < 30:
                self.delivery_fee = 2.99
            else:
                self.delivery_fee = 0.00
        else:
            self.delivery_fee = 0.00
        
        # Calculate tax (8%)
        self.tax = round(self.subtotal * 0.08, 2)
        
        # Calculate total
        self.total = round(self.subtotal + self.tax + self.delivery_fee, 2)
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_address": self.customer_address,
            "order_type": self.order_type,
            "items": self.items,
            "subtotal": f"${self.subtotal:.2f}",
            "tax": f"${self.tax:.2f}",
            "delivery_fee": f"${self.delivery_fee:.2f}",
            "total": f"${self.total:.2f}",
            "status": self.status,
            "special_instructions": self.special_instructions,
            "created_at": self.created_at.strftime("%Y-%m-%d %I:%M %p")
        }


# In-memory order storage (in production, use a database)
_orders = {}
_current_order = None


def start_new_order(customer_name: str, customer_phone: str, customer_address: str = None) -> Dict:
    """
    Start a new order for a customer
    
    Args:
        customer_name: Customer's name
        customer_phone: Customer's phone number
        customer_address: Delivery address (optional, for pickup orders)
    
    Returns:
        Dict with order confirmation
    """
    global _current_order
    
    order = Order(customer_name, customer_phone, customer_address)
    _current_order = order
    _orders[order.order_id] = order
    
    order_type = "delivery" if customer_address else "pickup"
    
    return {
        "success": True,
        "order_id": order.order_id,
        "message": f"Great! I've started a {order_type} order for {customer_name}. What would you like to order?",
        "order_type": order_type
    }


def add_pizza_to_order(pizza_name: str, size: str = "Large", quantity: int = 1, 
                       crust: str = "Classic Hand-Tossed", toppings: List[str] = None) -> Dict:
    """
    Add a pizza to the current order
    
    Args:
        pizza_name: Name of the pizza (e.g., "Pepperoni", "Supreme")
        size: Pizza size (Small, Medium, Large, Extra Large)
        quantity: Number of pizzas
        crust: Crust type
        toppings: Additional toppings
    
    Returns:
        Dict with confirmation
    """
    global _current_order
    
    if not _current_order:
        return {
            "success": False,
            "message": "Please start an order first by providing your name and phone number."
        }
    
    # Pizza prices (base prices for Large)
    pizza_prices = {
        "margherita": 12.99,
        "pepperoni": 14.99,
        "hawaiian": 15.99,
        "supreme": 17.99,
        "bbq chicken": 16.99,
        "veggie deluxe": 15.99,
        "meat lovers": 18.99,
        "buffalo chicken": 16.99,
        "truffle mushroom": 19.99,
        "prosciutto & arugula": 20.99
    }
    
    # Size multipliers
    size_multipliers = {
        "small": 0.7,
        "medium": 0.85,
        "large": 1.0,
        "extra large": 1.3
    }
    
    pizza_name_lower = pizza_name.lower()
    size_lower = size.lower()
    
    if pizza_name_lower not in pizza_prices:
        return {
            "success": False,
            "message": f"Sorry, I couldn't find '{pizza_name}' on our menu. Please check the menu and try again."
        }
    
    base_price = pizza_prices[pizza_name_lower]
    size_multiplier = size_multipliers.get(size_lower, 1.0)
    price = round(base_price * size_multiplier, 2)
    
    # Add crust upcharge
    crust_prices = {
        "thick pan crust": 2.00,
        "stuffed crust": 3.00,
        "gluten-free crust": 3.50
    }
    price += crust_prices.get(crust.lower(), 0.0)
    
    # Add topping charges
    if toppings:
        price += len(toppings) * 1.50
    
    # Build customization string
    customizations = []
    if crust.lower() != "classic hand-tossed":
        customizations.append(crust)
    if toppings:
        customizations.append(f"Extra: {', '.join(toppings)}")
    
    customization_str = " | ".join(customizations) if customizations else ""
    
    _current_order.add_item(pizza_name, size, quantity, price, customization_str)
    
    return {
        "success": True,
        "message": f"Added {quantity} {size} {pizza_name} pizza(s) to your order! Anything else?",
        "item_added": {
            "name": pizza_name,
            "size": size,
            "quantity": quantity,
            "price": f"${price:.2f}",
            "customizations": customization_str
        },
        "current_total": f"${_current_order.total:.2f}"
    }


def add_side_to_order(side_name: str, quantity: int = 1) -> Dict:
    """
    Add a side item to the current order
    
    Args:
        side_name: Name of the side (e.g., "Breadsticks", "Wings")
        quantity: Number of items
    
    Returns:
        Dict with confirmation
    """
    global _current_order
    
    if not _current_order:
        return {
            "success": False,
            "message": "Please start an order first by providing your name and phone number."
        }
    
    side_prices = {
        "breadsticks": 6.99,
        "garlic knots": 7.99,
        "chicken wings": 11.99,
        "wings": 11.99,
        "mozzarella sticks": 8.99,
        "caesar salad": 7.99,
        "garden salad": 6.99
    }
    
    side_name_lower = side_name.lower()
    
    if side_name_lower not in side_prices:
        return {
            "success": False,
            "message": f"Sorry, I couldn't find '{side_name}' on our menu."
        }
    
    price = side_prices[side_name_lower]
    _current_order.add_item(side_name, "Regular", quantity, price)
    
    return {
        "success": True,
        "message": f"Added {quantity} {side_name} to your order!",
        "current_total": f"${_current_order.total:.2f}"
    }


def add_drink_to_order(drink_name: str, quantity: int = 1) -> Dict:
    """Add a drink to the current order"""
    global _current_order
    
    if not _current_order:
        return {
            "success": False,
            "message": "Please start an order first."
        }
    
    drink_prices = {
        "soft drink": 2.99,
        "soda": 2.99,
        "coke": 2.99,
        "sprite": 2.99,
        "2-liter": 4.99,
        "water": 1.99,
        "iced tea": 2.99
    }
    
    price = drink_prices.get(drink_name.lower(), 2.99)
    _current_order.add_item(drink_name, "Regular", quantity, price)
    
    return {
        "success": True,
        "message": f"Added {quantity} {drink_name} to your order!",
        "current_total": f"${_current_order.total:.2f}"
    }


def review_current_order() -> Dict:
    """Review the current order"""
    global _current_order
    
    if not _current_order:
        return {
            "success": False,
            "message": "No active order. Start an order by providing your name and phone number."
        }
    
    if not _current_order.items:
        return {
            "success": False,
            "message": "Your order is empty. What would you like to add?"
        }
    
    return {
        "success": True,
        "order": _current_order.to_dict()
    }


def add_special_instructions(instructions: str) -> Dict:
    """Add special instructions to the order"""
    global _current_order
    
    if not _current_order:
        return {"success": False, "message": "No active order."}
    
    _current_order.special_instructions = instructions
    return {
        "success": True,
        "message": f"Special instructions added: {instructions}"
    }


def confirm_order() -> Dict:
    """Confirm and finalize the order"""
    global _current_order
    
    if not _current_order:
        return {
            "success": False,
            "message": "No active order to confirm."
        }
    
    if not _current_order.items:
        return {
            "success": False,
            "message": "Cannot confirm an empty order. Please add items first."
        }
    
    _current_order.status = "confirmed"
    order_summary = _current_order.to_dict()
    
    # Clear current order
    _current_order = None
    
    return {
        "success": True,
        "message": f"Order {order_summary['order_id']} confirmed! Your order will be ready in 30-45 minutes.",
        "order": order_summary
    }


def cancel_current_order() -> Dict:
    """Cancel the current order"""
    global _current_order
    
    if not _current_order:
        return {"success": False, "message": "No active order to cancel."}
    
    order_id = _current_order.order_id
    del _orders[order_id]
    _current_order = None
    
    return {
        "success": True,
        "message": "Order cancelled. Let me know if you'd like to start a new order!"
    }


def get_order_status(order_id: str) -> Dict:
    """Get the status of an order"""
    if order_id not in _orders:
        return {
            "success": False,
            "message": f"Order {order_id} not found."
        }
    
    order = _orders[order_id]
    return {
        "success": True,
        "order": order.to_dict()
    }
