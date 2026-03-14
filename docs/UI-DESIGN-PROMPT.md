# Pizza Restaurant AI Chat UI - Design Prompt

Copy and paste this prompt into your UI generation tool (v0.dev, bolt.new, etc.):

---

## PROMPT FOR UI GENERATOR:

Create a modern, responsive pizza restaurant website with an AI chatbot interface. The design should be warm, inviting, and food-focused.

### Design Requirements:

**Color Scheme:**
- Primary: Warm red/orange (#E74C3C or #FF6B35) - pizza/tomato inspired
- Secondary: Cream/beige (#FFF8E7) for backgrounds
- Accent: Dark brown (#2C1810) for text
- Success green for order confirmations
- Use food photography as hero images

**Layout:**

1. **Header/Navigation:**
   - Restaurant logo (left)
   - Navigation: Menu | Locations | Deals | Order Now
   - Phone number and "Call Us" button (right)
   - Sticky header on scroll

2. **Hero Section:**
   - Full-width background image of delicious pizza
   - Overlay text: "Fresh Pizza, Delivered Hot"
   - CTA button: "Order Now" (opens chat)
   - Secondary CTA: "View Menu"

3. **Chat Interface (Main Feature):**
   - Floating chat button (bottom right) with pizza emoji 🍕
   - When clicked, opens chat panel (slides in from right)
   - Chat panel should be 400px wide on desktop, full screen on mobile
   - Chat header: "Order Assistant" with minimize/close buttons
   - Message area with smooth scrolling
   - Input box at bottom with send button
   - Show typing indicator when AI is responding
   - Messages should have:
     * Customer messages: right-aligned, blue bubbles
     * AI messages: left-aligned, white bubbles with subtle shadow
     * Timestamps (small, gray text)
   - Quick action buttons: "View Menu", "Check Deals", "Track Order"

4. **Menu Preview Section:**
   - Grid of pizza cards (3 columns on desktop, 1 on mobile)
   - Each card shows:
     * Pizza image
     * Name and price
     * Brief description
     * "Add to Order" button (opens chat)
   - Categories: Classic | Specialty | Gourmet

5. **Features Section:**
   - 3 columns with icons:
     * 🚚 "30-Min Delivery" 
     * 💬 "AI Order Assistant"
     * 🎉 "Daily Deals"

6. **Footer:**
   - Store locations with addresses
   - Contact info
   - Social media links
   - Hours of operation

### Technical Requirements:

**Frontend Stack:**
- React with TypeScript
- Tailwind CSS for styling
- Framer Motion for animations
- React Icons for icons
- Axios for API calls

**Chat Component Features:**
```typescript
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

// API endpoint to connect to
const API_URL = 'http://localhost:8000/chat';

// Send message function
async function sendMessage(message: string) {
  const response = await axios.post(API_URL, { message });
  return response.data;
}
```

**Responsive Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Animations:**
- Chat panel slides in from right (300ms ease-out)
- Messages fade in with slight slide up
- Hover effects on buttons (scale 1.05)
- Smooth scroll behavior
- Loading spinner while AI responds

**Accessibility:**
- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus indicators
- Alt text on all images
- Color contrast ratio > 4.5:1

### Chat UI Specific Details:

**Message Bubbles:**
```css
User messages:
- Background: #3B82F6 (blue)
- Text: white
- Border radius: 18px 18px 4px 18px
- Max width: 70%
- Padding: 12px 16px

Bot messages:
- Background: white
- Text: #1F2937 (dark gray)
- Border: 1px solid #E5E7EB
- Border radius: 18px 18px 18px 4px
- Max width: 70%
- Padding: 12px 16px
- Box shadow: 0 1px 2px rgba(0,0,0,0.05)
```

**Input Box:**
- Height: 56px
- Border: 2px solid #E5E7EB
- Focus border: #3B82F6
- Placeholder: "Type your order or ask a question..."
- Send button: Blue circle with white arrow icon
- Emoji picker button (optional)

**Quick Reply Buttons:**
Show these as suggestions when chat opens:
- "🍕 Order Pizza"
- "📋 View Menu"
- "🎁 Current Deals"
- "📍 Store Locations"
- "⏰ Store Hours"

Style: Small pills with light gray background, hover effect

**Order Summary Card (in chat):**
When reviewing order, show a card with:
- Item list with quantities
- Subtotal, tax, delivery fee
- Total (bold, larger)
- "Confirm Order" button (green)
- "Modify Order" button (gray)

### Example Component Structure:

```
App
├── Header
├── Hero
├── ChatButton (floating)
├── ChatPanel
│   ├── ChatHeader
│   ├── MessageList
│   │   ├── Message (user)
│   │   ├── Message (bot)
│   │   └── TypingIndicator
│   ├── QuickReplies
│   └── ChatInput
├── MenuPreview
├── Features
└── Footer
```

### Additional Features:

1. **Order Tracking:**
   - Show order status in chat
   - Progress bar: Received → Preparing → Baking → Out for Delivery

2. **Menu Integration:**
   - Clicking menu items auto-fills chat with item name
   - Show item details in chat (image, price, description)

3. **Deal Notifications:**
   - Small banner at top showing current deal
   - Dismissible
   - "Tuesday Special: 20% off Large Pizzas!"

4. **Mobile Optimizations:**
   - Chat takes full screen on mobile
   - Swipe down to close
   - Bottom navigation bar
   - Tap to call button

### Sample Content:

**Hero Text:**
"Authentic Italian Pizza, Made Fresh Daily"
"Order in seconds with our AI assistant"

**Feature Cards:**
- "30-Minute Delivery or It's Free"
- "Chat with our AI to customize your perfect pizza"
- "New deals every Tuesday and weekend"

**Menu Items (examples):**
- Margherita Pizza - $12.99
- Pepperoni Classic - $14.99
- Supreme Deluxe - $17.99

### Design Inspiration:
- Modern food delivery apps (DoorDash, Uber Eats)
- Clean, minimal chat interfaces (Intercom, Drift)
- Warm, appetizing food photography
- Smooth animations and transitions

### Important Notes:
- Make it feel premium but approachable
- Food images should be high quality and appetizing
- Chat should feel conversational and helpful
- Mobile-first design approach
- Fast loading times
- Clear call-to-actions

---

## Additional Context for the AI:

This UI will connect to a FastAPI backend at `http://localhost:8000/chat` that accepts POST requests with `{"message": "user message"}` and returns `{"response": "bot response"}`.

The chat should handle:
- Taking orders (name, phone, address)
- Menu questions
- Recommendations
- Order review and confirmation
- Store information
- Delivery inquiries

Make it beautiful, functional, and easy to use! 🍕
