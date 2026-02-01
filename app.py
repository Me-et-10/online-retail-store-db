# app.py - Main Flask Application for Online Retail Store
from flask import Flask, render_template, request, redirect, url_for, flash
from database import create_tables, get_db_connection
from models import Customer, Product, Order, OrderItem
from forms import AddCustomerForm, AddProductForm, PlaceOrderForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # CHANGE THIS IN PRODUCTION!

# Initialize database tables on startup
with app.app_context():
    create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def customers():
    customers_list = Customer.all()
    return render_template('customers.html', customers=customers_list)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    form = AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data or None,
            address=form.address.data or None,
            city=form.city.data or None,
            state=form.state.data or None,
            zip_code=form.zip_code.data or None
        )
        customer.save()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html', form=form)

@app.route('/products')
def products():
    products_list = Product.all()
    return render_template('products.html', products=products_list)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            category=form.category.data
        )
        product.save()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('add_product.html', form=form)

@app.route('/orders/place', methods=['GET', 'POST'])
def place_order():
    form = PlaceOrderForm()
    customers_list = Customer.all()
    products_list = Product.all()
    form.customer_id.choices = [(c.customer_id, f"{c.first_name} {c.last_name}") for c in customers_list]
    form.product_id.choices = [(p.product_id, f"{p.name} (${p.price:.2f})") for p in products_list]

    if form.validate_on_submit():
        customer_id = form.customer_id.data
        product_id = form.product_id.data
        quantity = form.quantity.data

        product = Product.get(product_id)
        if not product or product.stock_quantity < quantity:
            flash('Invalid product or insufficient stock.', 'danger')
            return redirect(url_for('place_order'))

        total_amount = product.price * quantity
        order = Order(customer_id=customer_id, total_amount=total_amount, order_status='Processing')
        order.save()

        order_item = OrderItem(order_id=order.order_id, product_id=product.product_id, quantity=quantity, unit_price=product.price)
        order_item.save()
        
        product.stock_quantity -= quantity
        product.save()

        flash('Order placed successfully!', 'success')
        return redirect(url_for('view_orders'))
    
    return render_template('place_order.html', form=form, customers=customers_list, products=products_list)

@app.route('/orders')
def view_orders():
    orders_list = Order.all()
    # Enrich orders with customer and product names for display
    for order in orders_list:
        customer = Customer.get(order.customer_id)
        order.customer_name = f"{customer.first_name} {customer.last_name}" if customer else "Unknown"
        for item in order.items:
            product = Product.get(item.product_id)
            item.product_name = product.name if product else "Unknown Product"
    return render_template('view_orders.html', orders=orders_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
