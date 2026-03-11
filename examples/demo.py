#!/usr/bin/env python3
"""
Simple Pizza Agent Demo - Works without Ollama

This demo shows the tools working without needing a full LLM setup.
Use this to test the agent logic before running the full version.
"""

import sys
sys.path.append('.')

from workshop.tools import (
    get_pizza_quantity,
    get_estimated_delivery_time,
    check_store_hours,
    find_nearest_location,
    check_delivery_availability,
    get_special_deals,
    recommend_pizza
)


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def demo_tools():
    """Demonstrate all the pizza ordering tools"""
    
    print_header("Pizza Customer Service Agent - Tool Demo")
    
    print("\n1. Calculate Pizza Quantity")
    print("-" * 60)
    result = get_pizza_quantity(15)
    print(result)
    
    print("\n2. Get Estimated Delivery Time")
    print("-" * 60)
    result = get_estimated_delivery_time()
    print(result)
    
    print("\n3. Check Store Hours")
    print("-" * 60)
    result = check_store_hours("downtown")
    print(result)
    
    print("\n4. Find Nearest Location")
    print("-" * 60)
    result = find_nearest_location()
    print(result)
    
    print("\n5. Check Delivery Availability")
    print("-" * 60)
    result = check_delivery_availability("123 Main St")
    print(result)
    
    print("\n6. Get Special Deals")
    print("-" * 60)
    result = get_special_deals()
    print(result)
    
    print("\n7. Recommend Pizza (Vegetarian)")
    print("-" * 60)
    result = recommend_pizza("vegetarian")
    print(result)
    
    print("\n8. Recommend Pizza (Meat Lover)")
    print("-" * 60)
    result = recommend_pizza("meat lover")
    print(result)
    
    print_header("All Tools Working Successfully!")
    print("\nTo run the full AI agent, ensure Ollama is installed and running:")
    print("  1. Install Ollama: https://ollama.com")
    print("  2. Start Ollama: ollama serve")
    print("  3. Pull a model: ollama pull llama3.2")
    print("  4. Run agent: cd workshop && python agent.py")
    print()


def interactive_demo():
    """Simple interactive demo"""
    print_header("Pizza Customer Service - Interactive Demo")
    print("\nAvailable commands:")
    print("  quantity <number>  - Calculate pizzas needed")
    print("  delivery          - Get delivery estimate")
    print("  hours <location>  - Check store hours")
    print("  deals             - Show current deals")
    print("  recommend <type>  - Get pizza recommendations")
    print("  locations         - Show all locations")
    print("  help              - Show this help")
    print("  quit              - Exit")
    print()
    
    while True:
        try:
            user_input = input("Command: ").strip().lower()
            
            if not user_input:
                continue
            
            if user_input in ['quit', 'exit', 'q']:
                print("\nThanks for using Pizza Customer Service!")
                break
            
            parts = user_input.split(maxsplit=1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            
            print()
            
            if command == 'quantity':
                try:
                    people = int(args) if args else 10
                    print(get_pizza_quantity(people))
                except ValueError:
                    print("Please provide a number: quantity 15")
            
            elif command == 'delivery':
                print(get_estimated_delivery_time())
            
            elif command == 'hours':
                location = args if args else "downtown"
                print(check_store_hours(location))
            
            elif command == 'deals':
                print(get_special_deals())
            
            elif command == 'recommend':
                preference = args if args else "popular"
                print(recommend_pizza(preference))
            
            elif command == 'locations':
                print(find_nearest_location())
            
            elif command == 'help':
                print("Available commands:")
                print("  quantity <number>  - Calculate pizzas needed")
                print("  delivery          - Get delivery estimate")
                print("  hours <location>  - Check store hours")
                print("  deals             - Show current deals")
                print("  recommend <type>  - Get pizza recommendations")
                print("  locations         - Show all locations")
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\nThanks for using Pizza Customer Service!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo_tools()
    elif len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_demo()
    else:
        print("Pizza Customer Service Agent Demo")
        print("\nUsage:")
        print("  python demo.py --demo         # Show all tools")
        print("  python demo.py --interactive  # Interactive demo")
        print("\nOr run the full AI agent:")
        print("  cd workshop && python agent.py")


if __name__ == "__main__":
    main()
