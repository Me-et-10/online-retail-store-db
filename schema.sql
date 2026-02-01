-- Online Retail Store Database Schema

-- Table for Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Products
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table for Order Items (Junction table for orders and products)
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert Sample Data

-- Customers
INSERT INTO customers (first_name, last_name, email, phone_number, address, city, state, zip_code) VALUES
('Alice', 'Smith', 'alice.smith@example.com', '555-1234', '123 Main St', 'Anytown', 'CA', '90210'),
('Bob', 'Johnson', 'bob.j@example.com', '555-5678', '456 Oak Ave', 'Otherville', 'NY', '10001');

-- Products
INSERT INTO products (name, description, price, stock_quantity, category) VALUES
('Laptop Pro X', 'High-performance laptop with 16GB RAM and 512GB SSD.', 1200.00, 50, 'Electronics'),
('Wireless Mouse', 'Ergonomic wireless mouse with adjustable DPI.', 25.99, 200, 'Accessories'),
('Mechanical Keyboard', 'RGB mechanical keyboard with blue switches.', 89.99, 100, 'Accessories'),
('4K Monitor', '27-inch 4K UHD monitor with HDR support.', 350.00, 30, 'Electronics');

-- Orders
INSERT INTO orders (customer_id, total_amount, order_status) VALUES
(1, 1225.99, 'Processing'), -- Alice ordered Laptop and Mouse
(2, 89.99, 'Pending');       -- Bob ordered Keyboard

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1200.00), -- Alice: 1 Laptop Pro X
(1, 2, 1, 25.99),   -- Alice: 1 Wireless Mouse
(2, 3, 1, 89.99);    -- Bob: 1 Mechanical Keyboard
