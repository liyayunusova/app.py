from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'
bootstrap = Bootstrap(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define models
class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)


class Seller(db.Model):
    seller_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(50))
    quantity_in_total = db.Column(db.Integer)


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(120), db.ForeignKey('client.email'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('orders', lazy=True))
    manager = db.relationship('Manager', backref=db.backref('orders', lazy=True))


class CartItem(db.Model):  # renamed from Position2 to CartItem for clarity
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
    client = db.relationship('Client', backref=db.backref('cart_items', lazy=True))


# Routes
@app.route('/')
def base():
    return render_template('base.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)


@app.route('/cart')
def cart():
    if 'client_id' not in session:
        return redirect(url_for('login'))

    client_id = session['client_id']
    cart_items = CartItem.query.filter_by(client_id=client_id).all()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'client_id' not in session:
        return redirect(url_for('login'))

    client_id = session['client_id']
    cart_item = CartItem.query.filter_by(client_id=client_id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = CartItem(client_id=client_id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()
    return redirect(url_for('catalog'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        client = Client.query.filter_by(email=email, password=password).first()

        if client:
            session['client_id'] = client.client_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        existing_client = Client.query.filter_by(email=email).first()
        if existing_client:
            return render_template('register.html', error='Email already registered')

        new_client = Client(full_name=full_name, email=email, password=password)
        db.session.add(new_client)
        db.session.commit()
        session['client_id'] = new_client.client_id
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/view-data')
def view_data():
    products = Product.query.all()
    return render_template('view_data.html', products=products)


if __name__ == "__main__":
    with app.app_context():
        # Create the database and tables if they don't exist
        db.create_all()
        db.session.commit()

# Run the Flask app
app.run(host="0.0.0.0", debug=True)
