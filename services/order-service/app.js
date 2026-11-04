const express = require("express");
const { Pool } = require("pg");

const app = express();
app.use(express.json());

const pool = new Pool({
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || "devops_store",
    user: process.env.DB_USERNAME || "storeuser",
    password: process.env.DB_PASSWORD || "storepass123"
});

app.get("/api/orders", async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT
        o.id,
        o.customer_name,
        o.product_id,
        p.name AS product_name,
        o.quantity,
        o.status,
        o.created_at
    FROM orders o
    JOIN products p ON o.product_id = p.id
    ORDER BY o.id
     `);

        res.json(result.rows);
    } catch (error) {
        console.error("Failed to fetch orders:", error.message);
        res.status(500).json({ error: "Could not retrieve orders" });
    }
});

app.get("/api/orders/:id", async (req, res) => {
    try {
       const result = await pool.query(
    `SELECT
        o.id,
        o.customer_name,
        o.product_id,
        p.name AS product_name,
        o.quantity,
        o.status,
        o.created_at
     FROM orders o
     JOIN products p ON o.product_id = p.id
     WHERE o.id = $1`,
    [req.params.id]
);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: "Order not found" });
        }

        res.json(result.rows[0]);
    } catch (error) {
        console.error("Failed to fetch order:", error.message);
        res.status(500).json({ error: "Could not retrieve order" });
    }
});

app.get("/api/health", async (req, res) => {
    try {
        await pool.query("SELECT 1");
        res.json({ status: "healthy", database: "connected" });
    } catch (error) {
        res.status(500).json({ status: "unhealthy", database: "disconnected" });
    }
});

const port = process.env.PORT || 3000;

app.listen(port, "0.0.0.0", () => {
    console.log(`Order Service running on port ${port}`);
});