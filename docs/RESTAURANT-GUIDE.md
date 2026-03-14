# Restaurant Staff Guide - Pizza AI Agent

## Overview

This AI-powered pizza agent helps your restaurant take orders through:
- Website chat interface
- Phone integration (future)
- In-store kiosk (future)

## How It Works

### For Customers

1. Customer visits your website or calls
2. AI agent greets them and offers help
3. Agent takes their order step-by-step
4. Confirms order details and total
5. Processes payment (if integrated)
6. Sends order to kitchen system

### Current Features

- Natural conversation - customers can order naturally
- Menu recommendations based on preferences
- Order management (add, review, modify, confirm)
- Delivery/pickup options
- Special instructions
- Real-time pricing with tax and delivery fees
- Store hours and location info
- Current deals and promotions

## Using the System

### Starting the Application

```bash
# From project directory
source .venv/bin/activate
python3 launch.py
```

Access points:
- Customer interface: http://localhost:8501
- API backend: http://localhost:8000
- API documentation: http://localhost:8000/docs

### Example Customer Interactions

**Simple Order:**

```
Customer: "Hi, I want to order a pizza"
Agent: "I'd be happy to help! Can I get your name and phone number?"
Customer: "John Smith, 555-1234"
Agent: "Great! Is this for delivery or pickup?"
Customer: "Delivery to 123 Main St"
Agent: "Perfect! What would you like to order?"
Customer: "2 large pepperoni pizzas"
Agent: "Added 2 Large Pepperoni pizzas! Anything else?"
Customer: "That's all"
Agent: "Order confirmed! Total: $35.48. Ready in 30-45 minutes."
```

**With Recommendations:**
```
Customer: "What do you recommend for a vegetarian?"
Agent: "For vegetarians, I recommend: Veggie Deluxe, Margherita, or Truffle Mushroom"
Customer: "I'll take the Veggie Deluxe, large"
Agent: "Great choice! Added to your order."
```

## Customization for Your Restaurant

### Update Restaurant Information

Edit these files to match your restaurant:

1. **Menu** - `pizza_agent/knowledge/pizza_menu.md`
   - Update pizza names and prices
   - Add/remove items
   - Update sizes and options

2. **Store Locations** - `pizza_agent/knowledge/store_locations.md`
   - Add your actual locations
   - Update addresses and phone numbers
   - Set delivery zones

3. **Policies** - `pizza_agent/knowledge/policies_faq.md`
   - Update your policies
   - Add your FAQs
   - Set your hours

4. **Pricing** - `pizza_agent/tools/order_management.py`
   - Update pizza prices in the `pizza_prices` dictionary
   - Adjust tax rate (currently 8%)
   - Modify delivery fee structure

## Next Steps for Production

### Recommended Integrations

1. **Payment Processing**
   - Stripe, Square, or PayPal integration
   - Secure payment handling
   - Receipt generation

2. **Kitchen Display System**
   - Send orders directly to kitchen
   - Order tracking and status updates
   - Print tickets automatically

3. **Phone Integration**
   - Twilio for voice calls
   - Speech-to-text for phone orders
   - Automated order confirmation calls

4. **Database**
   - Replace in-memory storage with PostgreSQL/MySQL
   - Customer history and preferences
   - Order analytics

5. **SMS Notifications**
   - Order confirmation texts
   - Delivery status updates
   - Promotional messages

6. **Admin Dashboard**
   - View all orders
   - Manage menu items
   - Track sales and analytics
   - Customer management

## Support & Maintenance

### Common Issues

**Agent not responding:**
- Check GROQ_API_KEY in .env file
- Verify internet connection
- Check API rate limits

**Wrong prices:**
- Update prices in order_management.py
- Restart the application

**Menu items not found:**
- Ensure item names match exactly
- Update pizza_prices dictionary
- Check spelling in knowledge base

### Getting Help

For technical support or customization:
- Check documentation in /docs folder
- Review API docs at http://localhost:8000/docs
- Contact your development team

## Security Notes

- Never commit .env file with real API keys
- Use HTTPS in production
- Implement rate limiting
- Validate all customer inputs
- Secure payment information (PCI compliance)
- Regular security audits

---

Built with Groq AI, FastAPI, and Streamlit
