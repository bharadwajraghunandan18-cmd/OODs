
// ======================================
// ONLINE FOOD ORDERING SYSTEM
// JAVASCRIPT
// ======================================

// FOOD MENU
let foods = JSON.parse(localStorage.getItem("foods")) || [
    {
        id: 1,
        name: "Pizza",
        price: 200,
        category: "Fast Food",
        image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500"
    },
    {
        id: 2,
        name: "Burger",
        price: 120,
        category: "Fast Food",
        image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"
    },
    {
        id: 3,
        name: "Dosa",
        price: 60,
        category: "South Indian",
        image: "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=500"
    },
    {
        id: 4,
        name: "Biryani",
        price: 180,
        category: "Main Course",
        image: "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=500"
    },
    {
        id: 5,
        name: "Ice Cream",
        price: 80,
        category: "Dessert",
        image: "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500"
    }
];

// CART
let cart = JSON.parse(localStorage.getItem("cart")) || [];

// ORDERS
let orders = JSON.parse(localStorage.getItem("orders")) || [];


// SAVE DATA
function saveData() {
    localStorage.setItem("foods", JSON.stringify(foods));
    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("orders", JSON.stringify(orders));
}


// DISPLAY FOOD MENU
function displayFoods() {

    const foodList = document.getElementById("food-list");

    foodList.innerHTML = "";

    foods.forEach(food => {

        foodList.innerHTML += `
            <div class="food-card">

                <img src="${food.image}"
                     alt="${food.name}"
                     onerror="this.src='https://placehold.co/500x300?text=Food'">

                <h3>${food.name}</h3>

                <p>${food.category}</p>

                <div class="price">
                    ₹${food.price}
                </div>

                <button class="btn"
                    onclick="addToCart(${food.id})">
                    Add to Cart
                </button>

            </div>
        `;
    });
}


// ADD TO CART
function addToCart(id) {

    const food = foods.find(item => item.id === id);

    if (!food) return;

    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.quantity++;
    } else {
        cart.push({
            id: food.id,
            name: food.name,
            price: food.price,
            quantity: 1
        });
    }

    saveData();
    displayCart();

    alert(food.name + " added to cart!");
}


// REMOVE FROM CART
function removeFromCart(id) {

    const item = cart.find(item => item.id === id);

    if (item && item.quantity > 1) {
        item.quantity--;
    } else {
        cart = cart.filter(item => item.id !== id);
    }

    saveData();
    displayCart();
}


// DISPLAY CART
function displayCart() {

    const cartItems = document.getElementById("cart-items");

    cartItems.innerHTML = "";

    let total = 0;
    let count = 0;

    if (cart.length === 0) {
        cartItems.innerHTML = "<p>Your cart is empty!</p>";
    }

    cart.forEach(item => {

        const itemTotal = item.price * item.quantity;

        total += itemTotal;
        count += item.quantity;

        cartItems.innerHTML += `
            <div class="cart-item">

                <div>
                    <strong>${item.name}</strong>
                    <p>₹${item.price} × ${item.quantity}</p>
                    <p>Subtotal: ₹${itemTotal}</p>
                </div>

                <button class="remove-btn"
                    onclick="removeFromCart(${item.id})">
                    Remove
                </button>

            </div>
        `;
    });

    document.getElementById("total").textContent = total;

    document.getElementById("cart-count").textContent = count;
}


// SHOW CHECKOUT
function showCheckout() {

    if (cart.length === 0) {
        alert("Please add food items to your cart!");
        return;
    }

    document.getElementById("checkout")
        .scrollIntoView({ behavior: "smooth" });
}


// PLACE ORDER
document.getElementById("checkout-form")
.addEventListener("submit", function(event) {

    event.preventDefault();

    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const name = document.getElementById("customer-name").value.trim();

    const email = document.getElementById("customer-email").value.trim();

    const phone = document.getElementById("customer-phone").value.trim();

    const address = document.getElementById("customer-address").value.trim();

    const payment = document.getElementById("payment-method").value;

    const total = cart.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
    );

    // CREATE ORDER OBJECT
    const order = {

        id: Date.now(),

        customer: name,

        email: email,

        phone: phone,

        address: address,

        items: [...cart],

        total: total,

        payment: payment,

        paymentStatus:
            payment === "Cash"
                ? "Cash on Delivery"
                : "Successful",

        status: "Order Placed",

        date: new Date().toLocaleString()
    };

    // SAVE ORDER
    orders.push(order);

    // CLEAR CART
    cart = [];

    saveData();

    displayCart();
    displayOrders();

    // RESET FORM
    document.getElementById("checkout-form").reset();

    alert(
        "Order placed successfully!\n" +
        "Order ID: " + order.id +
        "\nTotal: ₹" + total
    );

    document.getElementById("orders")
        .scrollIntoView({ behavior: "smooth" });

});


// DISPLAY ORDERS
function displayOrders() {

    const orderList = document.getElementById("order-list");

    orderList.innerHTML = "";

    if (orders.length === 0) {
        orderList.innerHTML = "<p>No orders placed yet.</p>";
        return;
    }

    orders.slice().reverse().forEach(order => {

        const items = order.items.map(item =>
            `${item.name} × ${item.quantity}`
        ).join(", ");

        orderList.innerHTML += `

            <div class="order-card">

                <h3>Order #${order.id}</h3>

                <p><strong>Customer:</strong> ${order.customer}</p>

                <p><strong>Food:</strong> ${items}</p>

                <p><strong>Total:</strong> ₹${order.total}</p>

                <p><strong>Payment:</strong> ${order.payment}</p>

                <p><strong>Payment Status:</strong> ${order.paymentStatus}</p>

                <p><strong>Date:</strong> ${order.date}</p>

                <p><strong>Delivery Address:</strong> ${order.address}</p>

                <p><strong>Order Status:</strong>
                    <span>${order.status}</span>
                </p>

                <label>Update Order Status:</label>

                <select onchange="updateOrderStatus(${order.id}, this.value)">

                    <option value="Order Placed"
                        ${order.status === "Order Placed" ? "selected" : ""}>
                        Order Placed
                    </option>

                    <option value="Preparing"
                        ${order.status === "Preparing" ? "selected" : ""}>
                        Preparing
                    </option>

                    <option value="Out for Delivery"
                        ${order.status === "Out for Delivery" ? "selected" : ""}>
                        Out for Delivery
                    </option>

                    <option value="Delivered"
                        ${order.status === "Delivered" ? "selected" : ""}>
                        Delivered
                    </option>

                    <option value="Cancelled"
                        ${order.status === "Cancelled" ? "selected" : ""}>
                        Cancelled
                    </option>

                </select>

            </div>
        `;
    });
}


// UPDATE ORDER STATUS
function updateOrderStatus(id, status) {

    const order = orders.find(item => item.id === id);

    if (!order) return;

    if (order.status === "Delivered" ||
        order.status === "Cancelled") {

        alert("This order is already completed or cancelled.");
        displayOrders();
        return;
    }

    order.status = status;

    saveData();
    displayOrders();

    alert("Order status updated to: " + status);
}


// ADMIN - ADD FOOD ITEM
document.getElementById("admin-form")
.addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("food-name").value.trim();

    const price = Number(document.getElementById("food-price").value);

    const category = document.getElementById("food-category").value.trim();

    if (!name || !category || !Number.isFinite(price) || price <= 0) {
        alert("Please enter valid food details!");
        return;
    }

    const newFood = {

        id: foods.length > 0
            ? Math.max(...foods.map(food => food.id)) + 1
            : 1,

        name: name,

        price: price,

        category: category,

        image: "https://placehold.co/500x300?text=New+Food"
    };

    foods.push(newFood);

    saveData();

    displayFoods();

    document.getElementById("admin-form").reset();

    alert("New Food Item Added Successfully!");
});


// INITIALIZE WEBSITE
displayFoods();
displayCart();
displayOrders();
