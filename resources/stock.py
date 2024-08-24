from flask import Blueprint, jsonify, request
from models import Stock, Product
from db import db
from datetime import datetime

# Create a Blueprint
stock_bp = Blueprint('stock_bp', __name__)

# Insert a new stock entry
@stock_bp.route('/stock', methods=['POST'])
def insert_stock():
    data = request.get_json()
    product_id = data['product_id']
    product_quantity = data['product_quantity']
    last_purchase_rate = data['last_purchase_rate']

    # Check if the product exists in the Product table
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found in Product table!"}), 404

    new_stock = Stock(
        product_id=product_id,
        product_quantity=product_quantity,
        last_purchase_rate=last_purchase_rate,
        last_update_date=datetime.utcnow()
    )
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Stock entry added successfully!"}), 201

# Show all stock entries
@stock_bp.route('/stocks', methods=['GET'])
def show_stocks():
    stocks = Stock.query.all()
    output = []
    for stock in stocks:
        stock_data = {
            'id': stock.id,
            'product_id': stock.product_id,
            'product_name': stock.product.name,
            'product_quantity': stock.product_quantity,
            'last_purchase_rate': stock.last_purchase_rate,
            'last_update_date': stock.last_update_date
        }
        output.append(stock_data)
    return jsonify(output)

# Update an existing stock entry
@stock_bp.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.get_json()
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock entry not found!"}), 404
    
    stock.product_quantity = data.get('product_quantity', stock.product_quantity)
    stock.last_purchase_rate = data.get('last_purchase_rate', stock.last_purchase_rate)
    stock.last_update_date = datetime.utcnow()
    
    db.session.commit()
    return jsonify({"message": "Stock entry updated successfully!"})

# Delete a stock entry
@stock_bp.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock entry not found!"}), 404
    
    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock entry deleted successfully!"})
