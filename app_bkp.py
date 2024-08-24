from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from datetime import datetime
import os 


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////inventory.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost:5432/saheb_stone'

#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("Database_URL","sqlite:///data.db") # it will contain db details such as dbname, username, passwords
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Stock Table
class Stock(db.Model):
    __tablename__ = 'stock'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Stock {self.product_name} - {self.quantity}>"

# Purchase Table
class Purchase(db.Model):
    __tablename__ = 'purchase'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity_purchased = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Stock', backref=db.backref('purchases', lazy=True))
    
    def __repr__(self):
        return f"<Purchase {self.product_id} - {self.quantity_purchased}>"

class Sale(db.Model):
    __tablename__ = 'sale'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Stock', backref=db.backref('sales', lazy=True))
    
    def __repr__(self):
        return f"<Sale {self.product_id} - {self.quantity_sold}>"

# Endpoint to Add a Purchase Entry
@app.route('/add_purchase', methods=['POST'])
def add_purchase():
    data = request.json
    product_name = data.get('product_name')
    quantity_purchased = data.get('quantity_purchased')
    purchase_price = data.get('purchase_price')
    
    # Validate the input
    if not all([product_name, quantity_purchased, purchase_price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if the product exists in stock
    stock_item = Stock.query.filter_by(product_name=product_name).first()
    
    if stock_item:
        # If product exists, update the quantity
        stock_item.quantity += quantity_purchased
        stock_item.unit_price = purchase_price  # Optionally update the unit price
    else:
        # If product doesn't exist, add it to stock
        new_stock_item = Stock(
            product_name=product_name,
            quantity=quantity_purchased,
            unit_price=purchase_price
        )
        db.session.add(new_stock_item)
        db.session.flush()  # Flush to get the new stock item ID for purchase entry
        stock_item = new_stock_item
    
    # Create a new purchase entry
    new_purchase = Purchase(
        product_id=stock_item.id,
        quantity_purchased=quantity_purchased,
        purchase_price=purchase_price
    )
    
    db.session.add(new_purchase)
    db.session.commit()
    
    return jsonify({'message': 'Purchase entry added successfully and stock updated'}), 201

# Endpoint to Display Purchase Data
@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = Purchase.query.all()
    result = []
    
    for purchase in purchases:
        result.append({
            'id': purchase.id,
            'product_id': purchase.product_id,
            'quantity_purchased': purchase.quantity_purchased,
            'purchase_price': purchase.purchase_price,
            'purchase_date': purchase.purchase_date
        })
    
    return jsonify(result), 200

# Endpoint to Add a Sale Entry
@app.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.json
    product_name = data.get('product_name')
    quantity_sold = data.get('quantity_sold')
    sale_price = data.get('sale_price')
    
    # Validate the input
    if not all([product_name, quantity_sold, sale_price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if the product exists in stock
    stock_item = Stock.query.filter_by(product_name=product_name).first()
    
    if not stock_item:
        return jsonify({'error': 'Product not found in stock'}), 404
    
    # Check if there's enough stock to sell
    if stock_item.quantity < quantity_sold:
        return jsonify({'error': 'Insufficient stock for the sale'}), 400
    
    # Deduct the quantity sold from the stock
    stock_item.quantity -= quantity_sold
    
    # Create a new sale entry
    new_sale = Sale(
        product_id=stock_item.id,
        quantity_sold=quantity_sold,
        sale_price=sale_price
    )
    
    db.session.add(new_sale)
    db.session.commit()
    
    return jsonify({'message': 'Sale entry added successfully and stock updated'}), 201

# Endpoint to Display Sale Data
@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    result = []
    
    for sale in sales:
        result.append({
            'id': sale.id,
            'product_id': sale.product_id,
            'quantity_sold': sale.quantity_sold,
            'sale_price': sale.sale_price,
            'sale_date': sale.sale_date
        })
    
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within the application context
    app.run(debug=True)
