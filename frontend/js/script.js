document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');
    const cartBtn = document.getElementById('cart-btn');

    // API Configuration
    const API_BASE_URL = 'http://localhost:8000';

    // Toggle Chat Window
    chatToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
    });

    closeChat.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
    });

    // Navigate to Checkout
    if (cartBtn) {
        cartBtn.addEventListener('click', () => {
            window.location.href = 'checkout.html';
        });
    }

    // Handle Chat Submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to history
        addMessage(message, 'user');
        chatInput.value = '';

        // Show typing indicator or just wait
        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            if (data.success) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, I encountered an error: ' + (data.error || 'Unknown error'), 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Failed to connect to the AI assistant. Please ensure the backend is running.', 'bot');
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;

        const innerDiv = document.createElement('div');
        if (sender === 'user') {
            innerDiv.className = 'max-w-[80%] bg-blue-600 text-white rounded-2xl rounded-tr-none p-3 shadow-sm text-sm';
        } else {
            innerDiv.className = 'max-w-[80%] bg-white border border-gray-100 rounded-2xl rounded-tl-none p-3 shadow-sm text-sm';
        }
        innerDiv.textContent = text;

        messageDiv.appendChild(innerDiv);
        chatHistory.appendChild(messageDiv);

        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
