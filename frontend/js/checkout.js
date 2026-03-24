document.addEventListener('DOMContentLoaded', async () => {
    const orderItemsContainer = document.querySelector('.lg\\:col-span-5 .space-y-6.mb-8');
    const subtotalEl = document.querySelector('.space-y-3.border-t .flex:nth-child(1) span:nth-child(2)');
    const deliveryFeeEl = document.querySelector('.space-y-3.border-t .flex:nth-child(2) span:nth-child(2)');
    const taxEl = document.querySelector('.space-y-3.border-t .flex:nth-child(3) span:nth-child(2)');
    const totalEl = document.querySelector('.text-xl.font-black span:nth-child(2)');
    const placeOrderBtn = document.querySelector('button.w-full.bg-primary');

    // API Configuration
    const API_BASE_URL = 'http://localhost:8000';

    async function fetchOrder() {
        try {
            const response = await fetch(`${API_BASE_URL}/order`);
            const data = await response.json();
            if (data.success && data.order) {
                renderOrder(data.order);
            } else {
                console.log('No active order found or error:', data.message);
                // Optionally show a message that cart is empty
            }
        } catch (error) {
            console.error('Error fetching order:', error);
        }
    }

    function renderOrder(order) {
        // Clear existing static items
        orderItemsContainer.innerHTML = '';

        order.items.forEach(item => {
            const itemHtml = `
                <div class="flex gap-4">
                    <div class="w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 bg-orange-50 flex items-center justify-center text-4xl">
                        ${getEmoji(item.name)}
                    </div>
                    <div class="flex-1">
                        <div class="flex justify-between items-start">
                            <h3 class="font-bold">${item.name}</h3>
                            <span class="font-bold text-primary">$${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                        <p class="text-xs opacity-60 mt-1">${item.size} • ${item.customizations || 'Standard'}</p>
                        <div class="flex items-center gap-2 mt-2">
                            <span class="text-sm font-bold">Qty: ${item.quantity}</span>
                        </div>
                    </div>
                </div>
            `;
            orderItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
        });

        // Update totals
        subtotalEl.textContent = order.subtotal;
        deliveryFeeEl.textContent = order.delivery_fee === '$0.00' ? 'Free' : order.delivery_fee;
        taxEl.textContent = order.tax;
        totalEl.textContent = order.total;
        
        if (placeOrderBtn) {
            placeOrderBtn.innerHTML = `<span class="material-symbols-outlined">lock</span> Place Order • ${order.total}`;
        }
    }

    function getEmoji(name) {
        const n = name.toLowerCase();
        if (n.includes('margherita')) return '🍅';
        if (n.includes('pepperoni')) return '🍕';
        if (n.includes('mushroom') || n.includes('truffle')) return '🍄';
        if (n.includes('pesto') || n.includes('veggie')) return '🌿';
        if (n.includes('chicken')) return '🍗';
        if (n.includes('meat')) return '🥩';
        if (n.includes('hawaiian')) return '🍍';
        return '🍕';
    }

    // Handle Place Order
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: 'confirm order' })
                });
                const data = await response.json();
                if (data.success) {
                    alert('Order Placed Successfully! ' + data.response);
                    window.location.href = 'index.html';
                }
            } catch (error) {
                alert('Error placing order');
            }
        });
    }

    fetchOrder();
});
