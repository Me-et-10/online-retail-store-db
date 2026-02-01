# Online Retail Store Management Application (Flask)

This is a comprehensive web application built with Flask for managing an online retail store. It includes functionalities for customer management, product management, and order processing.

## Features

- **Customer Management:** Add, view, and manage customer details.
- **Product Management:** Add, view, and manage product details including stock quantity.
- **Order Processing:** Place new orders and view historical orders with detailed items.
- **SQLite Database:** Uses a SQLite database for data persistence.
- **Flask-WTF Forms:** For secure and validated user input.
- **Jinja2 Templates:** For dynamic web pages.

## Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Me-et-10/online-retail-store-db.git
    cd online-retail-store-db-code # Assuming this is your project directory
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database (create tables and add initial data):**
    ```bash
    python3 database.py
    ```

5.  **Run the Flask application:**
    ```bash
    flask --app app run --debug
    # Or python3 app.py
    ```

6.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
.venv/
├── app.py              # Main Flask application
├── database.py         # Handles SQLite connection and schema creation
├── forms.py            # Flask-WTF forms for input validation
├── models.py           # Defines data models (Customer, Product, Order, OrderItem)
├── requirements.txt    # Python dependencies
├── schema.sql          # SQL script for database schema
├── static/
│   └── style.css       # Basic styling for the web application
└── templates/
    ├── add_customer.html
    ├── add_product.html
    ├── base.html
    ├── customers.html
    ├── index.html
    ├── place_order.html
    ├── products.html
    └── view_orders.html
```
