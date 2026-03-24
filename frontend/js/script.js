document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');
    const cartBtn = document.getElementById('cart-btn');
    const cartCountEl = document.getElementById('cart-count');

    // API Configuration
    const API_BASE_URL = 'http://localhost:8000';

    // Global State
    let cart = JSON.parse(localStorage.getItem('pizza_cart')) || [];
    let chatMessages = JSON.parse(localStorage.getItem('chat_history')) || [];

    function updateCartUI() {
        if (cartCountEl) {
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            cartCountEl.textContent = totalItems;
        }
    }

    function addToCart(item) {
        const existing = cart.find(i => i.name === item.name && i.size === (item.size || 'Standard'));
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({ ...item, quantity: 1, size: item.size || 'Standard' });
        }
        localStorage.setItem('pizza_cart', JSON.stringify(cart));
        updateCartUI();
        
        // Visual Feedback
        const btn = document.querySelector(`[data-name="${item.name}"]`);
        if (btn) {
            const originalText = btn.textContent;
            btn.textContent = 'Added! ✅';
            btn.classList.add('bg-green-600');
            btn.classList.remove('bg-charcoal');
            setTimeout(() => {
                btn.textContent = originalText;
                btn.classList.remove('bg-green-600');
                btn.classList.add('bg-charcoal');
            }, 2000);
        }
    }

    // Initialize UI
    updateCartUI();
    loadChatHistory();

    // Event Listeners for Add to Cart Buttons
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-to-cart')) {
            const btn = e.target;
            const item = {
                name: btn.dataset.name,
                price: parseFloat(btn.dataset.price),
                size: btn.dataset.size,
                img: btn.dataset.img
            };
            addToCart(item);
        }
    });

    // Toggle Chat Window
    if (chatToggle) {
        chatToggle.addEventListener('click', () => {
            chatWindow.classList.toggle('hidden');
        });
    }

    if (closeChat) {
        closeChat.addEventListener('click', () => {
            chatWindow.classList.add('hidden');
        });
    }

    // Navigate to Checkout
    if (cartBtn) {
        cartBtn.addEventListener('click', () => {
            window.location.href = 'checkout.html';
        });
    }

    // Handle Chat Submission
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            chatInput.value = '';

            const lowerMsg = message.toLowerCase();

            // Client-side Intent Handling (calling & adding to cart)
            if (lowerMsg.includes('call') || lowerMsg.includes('phone') || lowerMsg.includes('number')) {
                simulateCall();
                return;
            }

            if (lowerMsg.includes('add') && lowerMsg.includes('cart')) {
                handleAddToCartIntent(lowerMsg);
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();
                if (data.success) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('Sorry, I encountered an error.', 'bot');
                }
            } catch (error) {
                addMessage('Failed to connect to the AI assistant.', 'bot');
            }
        });
    }

    function addMessage(text, sender, save = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2`;

        const innerDiv = document.createElement('div');
        if (sender === 'user') {
            innerDiv.className = 'max-w-[80%] bg-primary text-white rounded-2xl rounded-tr-none p-3 shadow-sm text-sm font-medium';
        } else {
            innerDiv.className = 'max-w-[80%] bg-white border border-gray-100 rounded-2xl rounded-tl-none p-3 shadow-sm text-sm text-charcoal';
        }
        innerDiv.innerHTML = text.replace(/\n/g, '<br>');

        messageDiv.appendChild(innerDiv);
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        if (save) {
            chatMessages.push({ text, sender });
            localStorage.setItem('chat_history', JSON.stringify(chatMessages));
        }
    }

    function loadChatHistory() {
        if (!chatHistory) return;
        chatHistory.innerHTML = '';
        if (chatMessages.length === 0) {
            addMessage("Hello! I'm your AI Taste Assistant. Looking for the perfect slice today?", 'bot', true);
        } else {
            chatMessages.forEach(msg => {
                addMessage(msg.text, msg.sender, false);
            });
        }
    }

    function simulateCall() {
        addMessage("<i>Initiating call to Artisan Pizza HQ...</i>", 'bot');
        setTimeout(() => {
            addMessage("<b>📞 Calling: +1 (555) 749-9224</b><br>Searching for available agents...", 'bot');
            setTimeout(() => {
                addMessage("<b>Connected!</b><br>'Hello! You're speaking with the Artisan Team. How can we help you today?'", 'bot');
            }, 2500);
        }, 1000);
    }

    function handleAddToCartIntent(msg) {
        // Simple regex matching for pizza names
        const pizzas = [
            { name: 'Truffle Mushroom', price: 24.00 },
            { name: 'Spicy Pepperoni', price: 22.00 },
            { name: 'Pesto Burrata', price: 26.00 }
        ];

        const found = pizzas.find(p => msg.includes(p.name.toLowerCase()));
        if (found) {
            addToCart(found);
            addMessage(`Excellent choice! I've added the <b>${found.name}</b> to your cart. 🛒`, 'bot');
        } else {
            addMessage("I can certainly help with that! Which pizza would you like to add? We have Truffle Mushroom, Spicy Pepperoni, and Pesto Burrata.", 'bot');
        }
    }
});
