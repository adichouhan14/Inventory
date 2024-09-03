from flask import Flask, request, jsonify, render_template
#from flask_sqlalchemy import SQLAlchemy
from models import *
# from models.product import Product
from db import db, product_unit
from flask_migrate import Migrate
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase import purchase_bp
from resources.sales import sales_bp
import os
from dotenv import load_dotenv
from resources.product import *
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_url")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration objects
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# Import Blueprints (assuming you have created these in separate files)
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase import purchase_bp
from resources.sales import sales_bp

# Register Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(sales_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products',  methods=['GET'])
def product():
    # products = Product.query.all()  #Fetch all products from the database
    # return render_template('product.html', products=products)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    products = pagination.items
    categories = Category.query.all()
    print('categories called from get product end point',categories)
    return render_template('product.html', categories=categories, products=products, product_unit=product_unit, pagination=pagination)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create tables within the application context
    app.run(debug=True)