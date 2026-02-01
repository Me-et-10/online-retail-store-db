# models.py - Defines data models and basic CRUD operations
from database import get_db_connection

class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None, phone_number=None, address=None, city=None, state=None, zip_code=None, registration_date=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.registration_date = registration_date

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.customer_id:
            # Update existing customer
            cursor.execute(
                "UPDATE customers SET first_name=?, last_name=?, email=?, phone_number=?, address=?, city=?, state=?, zip_code=? WHERE customer_id=?",
                (self.first_name, self.last_name, self.email, self.phone_number, self.address, self.city, self.state, self.zip_code, self.customer_id)
            )
        else:
            # Insert new customer
            cursor.execute(
                "INSERT INTO customers (first_name, last_name, email, phone_number, address, city, state, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.first_name, self.last_name, self.email, self.phone_number, self.address, self.city, self.state, self.zip_code)
            )
            self.customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get(customer_id):
        conn = get_db_connection()
        customer_data = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
        conn.close()
        if customer_data:
            return Customer(**customer_data)
        return None

    @staticmethod
    def all():
        conn = get_db_connection()
        customers_data = conn.execute("SELECT * FROM customers").fetchall()
        conn.close()
        return [Customer(**c) for c in customers_data]

    def __repr__(self):
        return f"<Customer {self.customer_id}: {self.first_name} {self.last_name} ({self.email})>"

class Product:
    def __init__(self, product_id=None, name=None, description=None, price=None, stock_quantity=None, category=None, created_at=None, updated_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category = category
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.product_id:
            cursor.execute(
                "UPDATE products SET name=?, description=?, price=?, stock_quantity=?, category=? WHERE product_id=?",
                (self.name, self.description, self.price, self.stock_quantity, self.category, self.product_id)
            )
        else:
            cursor.execute(
                "INSERT INTO products (name, description, price, stock_quantity, category) VALUES (?, ?, ?, ?, ?)",
                (self.name, self.description, self.price, self.stock_quantity, self.category)
            )
            self.product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get(product_id):
        conn = get_db_connection()
        product_data = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
        conn.close()
        if product_data:
            return Product(**product_data)
        return None

    @staticmethod
    def all():
        conn = get_db_connection()
        products_data = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        return [Product(**p) for p in products_data]

    def __repr__(self):
        return f"<Product {self.product_id}: {self.name} (${self.price:.2f})>"

class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None, total_amount=None, order_status=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.order_status = order_status
        self.items = [] # To hold OrderItem objects

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.order_id:
            cursor.execute(
                "UPDATE orders SET customer_id=?, total_amount=?, order_status=? WHERE order_id=?",
                (self.customer_id, self.total_amount, self.order_status, self.order_id)
            )
        else:
            cursor.execute(
                "INSERT INTO orders (customer_id, total_amount, order_status) VALUES (?, ?, ?)",
                (self.customer_id, self.total_amount, self.order_status)
            )
            self.order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get(order_id):
        conn = get_db_connection()
        order_data = conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
        if order_data:
            order = Order(**order_data)
            order_items_data = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
            order.items = [OrderItem(**item) for item in order_items_data]
            conn.close()
            return order
        conn.close()
        return None

    @staticmethod
    def all():
        conn = get_db_connection()
        orders_data = conn.execute("SELECT * FROM orders").fetchall()
        orders = [Order(**o) for o in orders_data]
        for order in orders:
            order_items_data = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order.order_id,)).fetchall()
            order.items = [OrderItem(**item) for item in order_items_data]
        conn.close()
        return orders

    def __repr__(self):
        return f"<Order {self.order_id} (Customer: {self.customer_id}, Total: ${self.total_amount:.2f})>"

class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=None, unit_price=None):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.order_item_id:
            cursor.execute(
                "UPDATE order_items SET order_id=?, product_id=?, quantity=?, unit_price=? WHERE order_item_id=?",
                (self.order_id, self.product_id, self.quantity, self.unit_price, self.order_item_id)
            )
        else:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (self.order_id, self.product_id, self.quantity, self.unit_price)
            )
            self.order_item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get_by_order(order_id):
        conn = get_db_connection()
        items_data = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
        conn.close()
        return [OrderItem(**item) for item in items_data]

    def __repr__(self):
        return f"<OrderItem {self.order_item_id}: Order {self.order_id}, Product {self.product_id}, Qty {self.quantity}>"
