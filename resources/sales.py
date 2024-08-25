from flask import Blueprint, jsonify, request
from db import db
from models import Sale, Stock, Product
from datetime import datetime

# Create a Blueprint
sales_bp = Blueprint('sales_bp', __name__)

# Insert a new sale entry
@sales_bp.route('/sale', methods=['POST'])
def insert_sale():
    data = request.get_json()
    product_id = data['product_id']
    sales_quantity = data['sales_quantity']
    sales_rate = data['sales_rate']
    sales_amount = sales_quantity * sales_rate

    # Check if the product exists in the Product table
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found in Product table!"}), 404

    # Insert into Sale table
    new_sale = Sale(
        product_id=product_id,
        sales_quantity=sales_quantity,
        sales_rate=sales_rate,
        sales_amount=sales_amount,
        sales_date=datetime.utcnow()
    )
    db.session.add(new_sale)
    db.session.commit()

    # Update the Stock table
    stock = Stock.query.get(product_id)
    if stock:
        stock.product_quantity -= sales_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0  # Prevent negative stock quantities
        stock.last_update_date = datetime.utcnow()
    else:
        return jsonify({"message": "Stock entry not found for the product!"}), 404

    db.session.commit()
    return jsonify({"message": "Sale entry added successfully and stock updated!"}), 201

# Show all sale entries
@sales_bp.route('/sales', methods=['GET'])
def show_sales():
    sales = Sale.query.all()
    output = []
    for sale in sales:
        sale_data = {
            'id': sale.id,
            'product_id': sale.product_id,
            'sales_quantity': sale.sales_quantity,
            'sales_rate': sale.sales_rate,
            'sales_amount': sale.sales_amount,
            'sales_date': sale.sales_date
        }
        output.append(sale_data)
    return jsonify(output)

# Update an existing sale entry
@sales_bp.route('/sale/<int:id>', methods=['PUT'])
def update_sale(id):
    data = request.get_json()
    sale = Sale.query.get(id)
    if not sale:
        return jsonify({"message": "Sale entry not found!"}), 404

    old_quantity = sale.sales_quantity
    old_rate = sale.sales_rate

    # Update the Sale table
    sale.product_id = data.get('product_id', sale.product_id)
    sale.sales_quantity = data.get('sales_quantity', sale.sales_quantity)
    sale.sales_rate = data.get('sales_rate', sale.sales_rate)
    sale.sales_amount = sale.sales_quantity * sale.sales_rate
    sale.sales_date = datetime.utcnow()

    db.session.commit()

    # Update the Stock table
    stock = Stock.query.get(sale.product_id)
    if stock:
        stock.product_quantity += old_quantity - sale.sales_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0  # Prevent negative stock quantities
        stock.last_update_date = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Sale entry updated successfully and stock adjusted!"})

# Delete a sale entry
@sales_bp.route('/sale/<int:id>', methods=['DELETE'])
def delete_sale(id):
    sale = Sale.query.get(id)
    if not sale:
        return jsonify({"message": "Sale entry not found!"}), 404

    # Update the Stock table
    stock = Stock.query.get(sale.product_id)
    if stock:
        stock.product_quantity += sale.sales_quantity  # Add the quantity back to stock
        stock.last_update_date = datetime.utcnow()

    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale entry deleted successfully and stock adjusted!"})
