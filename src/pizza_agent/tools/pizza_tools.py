from typing import Dict, List
from datetime import datetime, timedelta
import json


def get_pizza_quantity(people: int) -> str:
    """
    Calculate the number of pizzas to order based on the number of people.
    Assumes each pizza can feed 2-3 people depending on appetite.
    
    Args:
        people (int): The number of people to order pizza for
        
    Returns:
        str: Recommendation for number of pizzas to order
    """
    if people <= 0:
        return "Please provide a valid number of people (greater than 0)."
    
    # Calculate based on average appetite (assumes 2.5 people per large pizza)
    pizzas_needed = round(people / 2.5)
    
    # Minimum of 1 pizza
    if pizzas_needed < 1:
        pizzas_needed = 1
    
    suggestion = f"For {people} people, I recommend ordering {pizzas_needed} large pizza"
    if pizzas_needed > 1:
        suggestion += "s"
    suggestion += f" ({pizzas_needed} large pizzas should provide about {pizzas_needed * 8} slices)."
    
    # Add helpful tip
    if people > 5:
        suggestion += " For variety, consider ordering different flavors!"
    
    return suggestion


def calculate_order_total(items: List[Dict]) -> Dict:
    """
    Calculate the total cost of an order including tax and delivery.
    
    Args:
        items (List[Dict]): List of items with 'name', 'price', and 'quantity'
        
    Returns:
        Dict: Breakdown of costs including subtotal, tax, delivery fee, and total
    """
    subtotal = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    
    # Calculate delivery fee based on subtotal
    if subtotal < 15:
        delivery_fee = 4.99
    elif subtotal < 30:
        delivery_fee = 2.99
    else:
        delivery_fee = 0.00  # Free delivery over $30
    
    # Calculate tax (8% sales tax)
    tax = round(subtotal * 0.08, 2)
    
    # Calculate total
    total = round(subtotal + tax + delivery_fee, 2)
    
    return {
        "subtotal": f"${subtotal:.2f}",
        "tax": f"${tax:.2f}",
        "delivery_fee": f"${delivery_fee:.2f}",
        "total": f"${total:.2f}",
        "message": "Free delivery on orders over $30!" if delivery_fee > 0 else "Free delivery applied!"
    }


def get_estimated_delivery_time(order_time: str = None) -> str:
    """
    Estimate delivery time based on current time and typical preparation times.
    
    Args:
        order_time (str): Optional time string, defaults to current time
        
    Returns:
        str: Estimated delivery time range
    """
    if order_time is None:
        current_time = datetime.now()
    else:
        try:
            current_time = datetime.fromisoformat(order_time)
        except:
            current_time = datetime.now()
    
    # Check if it's peak hours (Friday-Saturday 6-8 PM)
    is_weekend = current_time.weekday() in [4, 5]  # Friday or Saturday
    is_peak_hours = 18 <= current_time.hour < 20
    
    if is_weekend and is_peak_hours:
        prep_time = 45
        delivery_window = 60
        message = "Peak hours - delivery may take a bit longer. "
    else:
        prep_time = 30
        delivery_window = 45
        message = ""
    
    estimated_time = current_time + timedelta(minutes=prep_time)
    max_time = current_time + timedelta(minutes=delivery_window)
    
    time_range = f"{estimated_time.strftime('%I:%M %p')} - {max_time.strftime('%I:%M %p')}"
    
    return f"{message}Estimated delivery: {time_range}"


def check_store_hours(location: str = "downtown", day: str = None) -> str:
    """
    Check if a store location is currently open and return hours.
    
    Args:
        location (str): Store location name (downtown, riverside, westside, eastend)
        day (str): Day of week, defaults to current day
        
    Returns:
        str: Store hours and current status
    """
    location = location.lower().strip()
    
    # Store hours database
    store_hours = {
        "downtown": {
            "weekday": "11:00 AM - 10:00 PM",
            "friday_saturday": "11:00 AM - 12:00 AM",
            "sunday": "12:00 PM - 9:00 PM"
        },
        "riverside": {
            "weekday": "11:00 AM - 10:00 PM",
            "friday_saturday": "11:00 AM - 11:00 PM",
            "sunday": "12:00 PM - 9:00 PM"
        },
        "westside": {
            "weekday": "10:00 AM - 9:00 PM",
            "saturday": "10:00 AM - 9:00 PM",
            "sunday": "11:00 AM - 7:00 PM"
        },
        "eastend": {
            "weekday": "11:00 AM - 10:00 PM",
            "friday_saturday": "11:00 AM - 12:00 AM",
            "sunday": "12:00 PM - 10:00 PM"
        }
    }
    
    # Normalize location names
    location_map = {
        "downtown": "downtown",
        "main": "downtown",
        "riverside": "riverside",
        "river": "riverside",
        "westside": "westside",
        "mall": "westside",
        "westside mall": "westside",
        "eastend": "eastend",
        "east end": "eastend",
        "east": "eastend"
    }
    
    location = location_map.get(location, "downtown")
    
    if location not in store_hours:
        return "Store location not found. Available locations: Downtown, Riverside, Westside Mall, East End."
    
    hours = store_hours[location]
    
    # Get current day if not specified
    if day is None:
        current_day = datetime.now().weekday()  # 0 = Monday, 6 = Sunday
    else:
        day = day.lower()
        day_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        current_day = day_map.get(day, datetime.now().weekday())
    
    # Determine which hours to show
    if current_day == 6:  # Sunday
        hours_today = hours.get("sunday", hours.get("weekday"))
    elif current_day in [4, 5]:  # Friday or Saturday
        hours_today = hours.get("friday_saturday", hours.get("weekday"))
    else:  # Monday-Thursday
        hours_today = hours.get("weekday")
    
    location_names = {
        "downtown": "Downtown",
        "riverside": "Riverside",
        "westside": "Westside Mall",
        "eastend": "East End"
    }
    
    return f"{location_names[location]} location hours today: {hours_today}"


def find_nearest_location(address: str = None) -> str:
    """
    Find the nearest Pizza store location (simulated).
    
    Args:
        address (str): Customer address
        
    Returns:
        str: Information about the nearest location
    """
    # In a real implementation, this would use geolocation
    # For now, we'll return a helpful response
    
    locations = """
Our Pizza Store Locations:

1. **Downtown** - 123 Main Street, Downtown
   Phone: (555) 123-4567
   Services: Dine-in, Takeout, Delivery

2. **Riverside** - 456 River Road, Riverside District
   Phone: (555) 234-5678
   Services: Dine-in, Takeout, Delivery

3. **Westside Mall** - 789 Shopping Center Blvd (Food Court)
   Phone: (555) 345-6789
   Services: Takeout only (no delivery)

4. **East End** - 321 Harbor Avenue, East End
   Phone: (555) 456-7890
   Services: Dine-in, Takeout, Delivery

All locations (except Westside Mall) deliver within a 5-mile radius.
"""
    
    if address:
        return f"To check if we deliver to '{address}', please call the location nearest to you:\n{locations}"
    else:
        return locations


def check_delivery_availability(address: str) -> str:
    """
    Check if delivery is available to a specific address.
    
    Args:
        address (str): Delivery address
        
    Returns:
        str: Delivery availability information
    """
    # In a real implementation, this would check against a delivery zone database
    # For this demo, we'll provide a helpful response
    
    return f"""To verify delivery to '{address}', please:

1. Call your nearest Pizza store location
2. Use our website: www.pizzaonline.com (enter your address)
3. Use our mobile app for instant delivery zone checking

Delivery Information:
- Orders under $15: $4.99 delivery fee
- Orders $15-$30: $2.99 delivery fee  
- Orders over $30: FREE delivery
- Typical delivery time: 30-45 minutes
- All locations deliver within a 5-mile radius (except Westside Mall)
"""


def get_special_deals() -> str:
    """
    Get current special deals and promotions.
    
    Returns:
        str: Information about current deals
    """
    deals = """
**Current Pizza Deals**

**Tuesday Special**
- 20% off all Large Pizzas every Tuesday!

**Student Discount**
- 15% off with valid student ID

**Senior Discount**  
- 10% off for customers 60+ years old

**Military Discount**
- 15% off with military ID

**Combo Deals:**
- Family Deal: $39.99 - 2 Large Pizzas, 1 Side, 2-Liter Drink
- Party Pack: $69.99 - 4 Large Pizzas, 2 Sides, Breadsticks, 2 2-Liter Drinks
- Date Night Special: $24.99 - 1 Medium Pizza, 2 Desserts, 2 Soft Drinks

**Delivery Special:**
- FREE delivery on orders over $30!

**Rewards Program:**
- Earn 1 point per $1 spent
- 100 points = $10 off
- Birthday reward: Free dessert
- Sign up at www.pizzaonline.com/rewards

Note: One coupon/discount per order. Cannot be combined with other offers.
"""
    return deals


def recommend_pizza(preferences: str) -> str:
    """
    Recommend pizzas based on customer preferences.
    
    Args:
        preferences (str): Customer preferences (vegetarian, meat lover, spicy, etc.)
        
    Returns:
        str: Pizza recommendations
    """
    preferences = preferences.lower()
    
    recommendations = []
    
    if "vegetarian" in preferences or "veggie" in preferences or "no meat" in preferences:
        recommendations.append("- **Veggie Deluxe** ($15.99) - Fresh vegetables including bell peppers, onions, mushrooms, tomatoes, and olives")
        recommendations.append("- **Margherita** ($12.99) - Classic Italian with fresh mozzarella and basil")
        recommendations.append("- **Truffle Mushroom** ($19.99) - Gourmet option with mixed mushrooms and truffle oil")
    
    if "meat" in preferences or "protein" in preferences:
        recommendations.append("- **Meat Lovers** ($18.99) - Loaded with pepperoni, sausage, bacon, ham, and beef")
        recommendations.append("- **Supreme** ($17.99) - Pepperoni, Italian sausage, peppers, onions, mushrooms, and olives")
        recommendations.append("- **Pepperoni** ($14.99) - Classic favorite with premium pepperoni")
    
    if "spicy" in preferences or "hot" in preferences or "buffalo" in preferences:
        recommendations.append("- **Buffalo Chicken** ($16.99) - Spicy buffalo sauce with grilled chicken and red onions")
        recommendations.append("- Tip: Add jalapeños to any pizza for extra heat! (+$1.50)")
    
    if "chicken" in preferences:
        recommendations.append("- **BBQ Chicken** ($16.99) - Grilled chicken with BBQ sauce, red onions, and cilantro")
        recommendations.append("- **Buffalo Chicken** ($16.99) - Spicy buffalo sauce with grilled chicken")
    
    if "gourmet" in preferences or "fancy" in preferences or "premium" in preferences:
        recommendations.append("- **Truffle Mushroom** ($19.99) - White sauce, mixed mushrooms, truffle oil, arugula")
        recommendations.append("- **Prosciutto & Arugula** ($20.99) - Prosciutto, fresh arugula, parmesan shavings")
    
    if not recommendations:
        # Default recommendations
        recommendations.append("- **Pepperoni** ($14.99) - Our most popular classic pizza")
        recommendations.append("- **Supreme** ($17.99) - Loaded with toppings for variety")
        recommendations.append("- **BBQ Chicken** ($16.99) - Customer favorite specialty pizza")
    
    result = f"Based on your preferences ({preferences}), here are my recommendations:\n\n"
    result += "\n".join(recommendations)
    result += "\n\nAll pizzas available in multiple sizes with various crust options!"
    
    return result


# Tool definitions for LangChain
TOOL_DEFINITIONS = [
    {
        "name": "get_pizza_quantity",
        "description": "Calculate how many pizzas to order based on the number of people. Use this when a customer asks how many pizzas they need for a group.",
        "parameters": {
            "type": "object",
            "properties": {
                "people": {
                    "type": "integer",
                    "description": "The number of people who will be eating pizza"
                }
            },
            "required": ["people"]
        }
    },
    {
        "name": "calculate_order_total",
        "description": "Calculate the total cost of an order including tax and delivery fees. Use when customer wants to know the total price.",
        "parameters": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "List of items with name, price, and quantity"
                }
            },
            "required": ["items"]
        }
    },
    {
        "name": "get_estimated_delivery_time",
        "description": "Get estimated delivery time for an order. Use when customer asks how long delivery will take.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_time": {
                    "type": "string",
                    "description": "Optional order time in ISO format, defaults to current time"
                }
            }
        }
    },
    {
        "name": "check_store_hours",
        "description": "Check store hours for a specific location. Use when customer asks about store hours or if a location is open.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Store location: downtown, riverside, westside, or eastend"
                },
                "day": {
                    "type": "string",
                    "description": "Day of week, defaults to current day"
                }
            }
        }
    },
    {
        "name": "find_nearest_location",
        "description": "Find Pizza store locations. Use when customer asks where stores are located or which store is nearest.",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "Optional customer address"
                }
            }
        }
    },
    {
        "name": "check_delivery_availability",
        "description": "Check if delivery is available to an address. Use when customer asks if we deliver to their location.",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "Delivery address to check"
                }
            },
            "required": ["address"]
        }
    },
    {
        "name": "get_special_deals",
        "description": "Get information about current deals and promotions. Use when customer asks about specials, deals, or discounts.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "recommend_pizza",
        "description": "Recommend pizzas based on customer preferences. Use when customer is unsure what to order or asks for suggestions.",
        "parameters": {
            "type": "object",
            "properties": {
                "preferences": {
                    "type": "string",
                    "description": "Customer preferences like vegetarian, meat lover, spicy, etc."
                }
            },
            "required": ["preferences"]
        }
    }
]


# Map function names to actual functions
TOOL_FUNCTIONS = {
    "get_pizza_quantity": get_pizza_quantity,
    "calculate_order_total": calculate_order_total,
    "get_estimated_delivery_time": get_estimated_delivery_time,
    "check_store_hours": check_store_hours,
    "find_nearest_location": find_nearest_location,
    "check_delivery_availability": check_delivery_availability,
    "get_special_deals": get_special_deals,
    "recommend_pizza": recommend_pizza
}
