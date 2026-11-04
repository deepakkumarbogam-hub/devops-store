CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    reviewer_name VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (name, description, price, stock) VALUES
('Laptop', 'High-performance laptop for development', 65000.00, 12),
('Mechanical Keyboard', 'RGB mechanical keyboard', 3500.00, 25),
('Wireless Mouse', 'Ergonomic wireless mouse', 1200.00, 40)
ON CONFLICT DO NOTHING;

INSERT INTO reviews (product_id, reviewer_name, rating, comment) VALUES
(1, 'Rahul', 5, 'Excellent laptop for development'),
(2, 'Priya', 4, 'Great keyboard, feels premium'),
(3, 'Arjun', 5, 'Very comfortable mouse');

INSERT INTO orders (customer_name, product_id, quantity, status) VALUES
('Rahul Sharma', 1, 1, 'Delivered'),
('Priya Reddy', 2, 2, 'Processing'),
('Arjun Kumar', 3, 1, 'Pending');