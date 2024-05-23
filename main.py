from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a simple model for demonstration
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

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
    return render_template('cart.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/view-data')
def view_data():
    products = Product.query.all()
    return render_template('view_data.html', products=products)

if __name__ == "__main__":
    with app.app_context():
        # Create the database and tables if they don't exist
        db.create_all()

        # Insert some sample data if the table is empty
        if Product.query.count() == 0:
            sample_products = [
                Product(name='Product 1', price=10.99),
                Product(name='Product 2', price=12.99),
                Product(name='Product 3', price=15.99)
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()

    # Run the Flask app
    app.run(host="0.0.0.0", debug=True)
