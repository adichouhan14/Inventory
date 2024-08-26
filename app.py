from flask import Flask, request, jsonify, render_template
#from flask_sqlalchemy import SQLAlchemy
from models import __init__
from db import db
from flask_migrate import Migrate
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase import purchase_bp
from resources.sales import sales_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_url")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(sales_bp)


migrate = Migrate(app, db)

# In-memory data stores for demonstration
products = []
purchases = []
stock = []
sales = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('products.html')

@app.route('/purchase')
def purchase():
    return render_template('purchases.html')

@app.route('/stock')
def stock():
    return render_template('stocks.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/sales', methods=['POST'])
def add_sales():
    data = request.json
    sales.append(data)
    return jsonify({"message": "Sale recorded successfully!"}), 201

@app.route('/stock', methods=['POST'])
def add_stock():
    data = request.json
    stock.append(data)
    return jsonify({"message": "Stock updated successfully!"}), 201

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create tables within the application context
    app.run(debug=True)