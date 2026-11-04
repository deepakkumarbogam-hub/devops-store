const express = require("express");

const app = express();

app.use(express.json());

const orders = [
    {
        id: 1,
        customer: "Rahul",
        product: "Laptop",
        quantity: 1,
        status: "Delivered"
    },
    {
        id: 2,
        customer: "Priya",
        product: "Mobile",
        quantity: 2,
        status: "Processing"
    },
    {
        id: 3,
        customer: "Arjun",
        product: "Headphones",
        quantity: 1,
        status: "Shipped"
    }
];

app.get("/api/orders", (req, res) => {
    res.json(orders);
});

app.get("/api/orders/:id", (req, res) => {

    const orderId = parseInt(req.params.id);

    const order = orders.find(o => o.id === orderId);

    if (!order) {
        return res.status(404).json({
            error: "Order not found"
        });
    }

    res.json(order);
});

app.get("/api/health", (req, res) => {
    res.json({
        status: "UP",
        service: "order-service"
    });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Order service running on port ${PORT}`);
});

