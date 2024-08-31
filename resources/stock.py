from flask import Blueprint, jsonify, request, render_template
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
    
    # Check if the product exists in the Product table
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found in Product table!"}), 404

    new_stock = Stock(
        product_id=product_id,
        product_quantity=product_quantity,
        last_update_date=datetime.utcnow()
    )
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Stock entry added successfully!"}), 201

# Show all stock entries
@stock_bp.route('/stocks', methods=['GET'])
def show_stocks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Stock.query.paginate(page=page, per_page=per_page, error_out=False)
    
    stocks = pagination.items
    for stock in stocks:
        stock.name = stock.product.name

    return render_template('stocks.html', stocks=stocks, pagination=pagination)

# Update an existing stock entry
@stock_bp.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.get_json()
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock entry not found!"}), 404
    
    stock.product_quantity = data.get('product_quantity', stock.product_quantity)
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
