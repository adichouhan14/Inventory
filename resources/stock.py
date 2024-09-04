from flask import Blueprint, jsonify, request, render_template
from models import Stock, Product
from db import db,product_unit
from datetime import datetime

# Create a Blueprint
stock_bp = Blueprint('stock_bp', __name__)

# Insert a new stock entry
@stock_bp.route('/stock', methods=['POST'])
def insert_stock():
    data = request.form
    print('data stock post method -->>',data)
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
        stock.unit = product_unit[stock.product.unit]
    products = Product.query.all()
    return render_template('stocks.html', stocks=stocks, products=products, pagination=pagination)

# Update an existing stock entry
# @stock_bp.route('/stock/<int:id>', methods=['PUT'])
# def update_stock(id):
#     data = request.get_json()
#     stock = Stock.query.get(id)
#     if not stock:
#         return jsonify({"message": "Stock entry not found!"}), 404
    
#     stock.product_quantity = data.get('product_quantity', stock.product_quantity)
#     stock.last_update_date = datetime.utcnow()
    
#     db.session.commit()
#     return jsonify({"message": "Stock entry updated successfully!"})

@stock_bp.route('/stock/<int:id>', methods=['GET', 'PUT'])
def update_stock(id):
    if request.method == 'GET':
        stock = Stock.query.get(id)
        if not stock:
            return jsonify({"message": "Stock entry not found!"}), 404

        stock_data = {
            'id': stock.id,
            'product_id': stock.product_id,
            'product_name': stock.product.name,
            'product_quantity': stock.product_quantity,
            'last_update_date': stock.last_update_date.strftime('%Y-%m-%d')
        }
        return jsonify(stock_data), 200

    # Handle the PUT method for updating the stock entry
    try:
        data = request.get_json()
        stock = Stock.query.get(id)
        if not stock:
            return jsonify({"message": "Stock entry not found!"}), 404
        stock.product_id = data.get('product_id', stock.product_id)
        stock.product_quantity = data.get('product_quantity', stock.product_quantity)
        stock.last_update_date = datetime.utcnow()
        
        db.session.commit()
        return jsonify({"message": "Stock entry updated successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Stock entry cannot be updated!"}), 404
        



# Delete a stock entry
@stock_bp.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock entry not found!"}), 404
    
    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock entry deleted successfully!"})

# Filter stock
@stock_bp.route('/stock/filter')
def filter_stock():
    print('In stock filter')
    query = request.args.get('query', '', type=str).strip()

    # Separate query by ID if it's numeric
    if query.isdigit():
        filtered_stock = Stock.query.filter(Stock.id == int(query)).all()
        print('filtered_stock id-->', filtered_stock)
    else:
        filtered_stock = Stock.query.join(Product).filter(Product.name.ilike(f'%{query}%')).all()
        print('filtered_stock-->', filtered_stock)

    stock_list = [{
        'id': stock.id,
        'name': stock.product.name,
        'product_quantity': stock.product_quantity,
        'last_update_date': stock.last_update_date.strftime('%Y-%m-%d')
    } for stock in filtered_stock]
    
    print('stock_list-->', stock_list)
    return jsonify(stocks=stock_list)