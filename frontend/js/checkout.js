document.addEventListener('DOMContentLoaded', async () => {
    const orderItemsContainer = document.querySelector('.lg\\:col-span-5 .space-y-6.mb-8');
    const subtotalEl = document.querySelector('.space-y-3.border-t .flex:nth-child(1) span:nth-child(2)');
    const deliveryFeeEl = document.querySelector('.space-y-3.border-t .flex:nth-child(2) span:nth-child(2)');
    const taxEl = document.querySelector('.space-y-3.border-t .flex:nth-child(3) span:nth-child(2)');
    const totalEl = document.querySelector('.text-xl.font-black span:nth-child(2)');
    const placeOrderBtn = document.querySelector('button.w-full.bg-primary');

    // API Configuration
    const API_BASE_URL = 'http://localhost:8000';

    // Get Cart from Local Storage
    let cart = JSON.parse(localStorage.getItem('pizza_cart')) || [];

    function renderOrder() {
        if (!orderItemsContainer) return;
        
        orderItemsContainer.innerHTML = '';
        let subtotal = 0;

        if (cart.length === 0) {
            orderItemsContainer.innerHTML = '<p class="text-gray-500 text-center py-8">Your cart is empty.</p>';
            updateTotals(0);
            return;
        }

        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;

            const itemHtml = `
                <div class="flex gap-4 items-center">
                    <div class="w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 bg-orange-50 flex items-center justify-center">
                        <i data-lucide="pizza" class="w-10 h-10 text-primary"></i>
                    </div>
                    <div class="flex-1">
                        <div class="flex justify-between items-start">
                            <h3 class="font-bold">${item.name}</h3>
                            <span class="font-bold text-primary">$${itemTotal.toFixed(2)}</span>
                        </div>
                        <p class="text-xs opacity-60 mt-1">${item.size || 'Standard'}</p>
                        <div class="flex items-center gap-2 mt-2">
                            <span class="text-sm font-bold">Qty: ${item.quantity}</span>
                        </div>
                    </div>
                </div>
            `;
            orderItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
        });

        updateTotals(subtotal);
        if (window.lucide) lucide.createIcons();
    }

    function updateTotals(subtotal) {
        const deliveryFee = subtotal > 0 ? 5.00 : 0;
        const tax = subtotal * 0.08;
        const total = subtotal + deliveryFee + tax;

        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        deliveryFeeEl.textContent = deliveryFee === 0 ? '$0.00' : `$${deliveryFee.toFixed(2)}`;
        taxEl.textContent = `$${tax.toFixed(2)}`;
        totalEl.textContent = `$${total.toFixed(2)}`;
        
        if (placeOrderBtn) {
            placeOrderBtn.innerHTML = `Place Order • $${total.toFixed(2)}`;
            placeOrderBtn.disabled = cart.length === 0;
            if (cart.length === 0) placeOrderBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
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
                    localStorage.removeItem('pizza_cart');
                    window.location.href = 'index.html';
                }
            } catch (error) {
                alert('Error placing order');
            }
        });
    }

    renderOrder();
});
