-- E-COMMERCE DATABASE SCHEMA
-- Save this as 'schema.sql' in your project folder

-- Customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    country TEXT NOT NULL,
    signup_date DATE NOT NULL,
    lifetime_value DECIMAL(10,2) DEFAULT 0.00
);

-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    supplier TEXT
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Order items table (line items for each order)
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample data for testing
INSERT INTO customers (name, email, country, signup_date, lifetime_value) VALUES
    ('Acme Corporation', 'contact@acme.com', 'USA', '2024-01-15', 12450.00),
    ('TechStart Solutions', 'hello@techstart.io', 'Canada', '2024-02-20', 8730.50),
    ('Global Traders Ltd', 'orders@globaltraders.co.uk', 'UK', '2024-03-10', 15200.75),
    ('Asia Pacific Exports', 'info@asiapac.sg', 'Singapore', '2024-04-05', 6200.00),
    ('Euro Retail GmbH', 'sales@euroretail.de', 'Germany', '2024-01-30', 9800.25);

INSERT INTO products (name, category, price, stock_quantity, supplier) VALUES
    ('Laptop Pro 15"', 'Electronics', 1299.99, 45, 'TechSupply Co'),
    ('Wireless Mouse', 'Accessories', 29.99, 230, 'TechSupply Co'),
    ('USB-C Hub 7-in-1', 'Accessories', 79.99, 120, 'GadgetWorld'),
    ('27" 4K Monitor', 'Electronics', 449.99, 28, 'DisplayMasters'),
    ('Mechanical Keyboard', 'Accessories', 129.99, 85, 'KeyTech'),
    ('Noise Cancelling Headphones', 'Audio', 199.99, 62, 'AudioPro'),
    ('Smartphone Stand', 'Accessories', 19.99, 310, 'GadgetWorld'),
    ('External SSD 1TB', 'Storage', 119.99, 94, 'DataStore Inc');

INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
    (1, '2025-01-10', 'delivered', 1459.97),
    (1, '2025-02-15', 'delivered', 349.98),
    (2, '2025-01-22', 'delivered', 879.98),
    (2, '2025-03-05', 'shipped', 1299.99),
    (3, '2025-01-05', 'delivered', 2499.95),
    (3, '2025-02-28', 'delivered', 599.97),
    (4, '2025-03-15', 'pending', 119.99),
    (5, '2025-02-10', 'delivered', 649.98),
    (5, '2025-03-20', 'shipped', 199.99);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1299.99), (1, 5, 1, 129.99), (1, 2, 1, 29.99),
    (2, 3, 2, 79.99), (2, 6, 1, 199.99),
    (3, 4, 1, 449.99), (3, 8, 1, 119.99), (3, 5, 2, 129.99),
    (4, 1, 1, 1299.99),
    (5, 1, 1, 1299.99), (5, 4, 1, 449.99), (5, 6, 1, 199.99), (5, 8, 2, 119.99),
    (6, 6, 3, 199.99),
    (7, 8, 1, 119.99),
    (8, 4, 1, 449.99), (8, 6, 1, 199.99),
    (9, 6, 1, 199.99);