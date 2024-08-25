from flask import Blueprint, jsonify, request
from db import db
from models import Purchase, Stock, Product
from datetime import datetime

# Create a Blueprint
purchase_bp = Blueprint('purchase_bp', __name__)

# Insert a new purchase entry
@purchase_bp.route('/purchase', methods=['POST'])
def insert_purchase():
    data = request.get_json()
    product_id = data['product_id']
    purchase_quantity = data['purchase_quantity']
    purchase_rate = data['purchase_rate']
    purchase_amount = purchase_quantity * purchase_rate

    # Check if the product exists in the Product table
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found in Product table!"}), 404

    # Insert into Purchase table
    new_purchase = Purchase(
        product_id=product_id,
        purchase_quantity=purchase_quantity,
        purchase_rate=purchase_rate,
        purchase_amount=purchase_amount,
        purchase_date=datetime.utcnow()
    )
    db.session.add(new_purchase)
    # Update the Stock table
    stock = Stock.query.get(product_id)
    if stock:
        stock.product_quantity += purchase_quantity
        stock.last_update_date = datetime.utcnow()
    else:
        # Create new stock if it doesn't exist
        new_stock = Stock(
            product_id=product_id,
            product_quantity=purchase_quantity,
            last_update_date=datetime.utcnow()
        )
        db.session.add(new_stock)

    db.session.commit()
    return jsonify({"message": "Purchase entry added successfully and stock updated!"}), 201

# Show all purchase entries
@purchase_bp.route('/purchases', methods=['GET'])
def show_purchases():
    purchases = Purchase.query.all()
    output = []
    for purchase in purchases:
        purchase_data = {
            'id': purchase.id,
            'product_id': purchase.product_id,
            'purchase_quantity': purchase.purchase_quantity,
            'purchase_rate': purchase.purchase_rate,
            'purchase_amount': purchase.purchase_amount,
            'purchase_date': purchase.purchase_date
        }
        output.append(purchase_data)
    return jsonify(output)

# Update an existing purchase entry
@purchase_bp.route('/purchase/<int:id>', methods=['PUT'])
def update_purchase(id):
    data = request.get_json()
    purchase = Purchase.query.get(id)
    if not purchase:
        return jsonify({"message": "Purchase entry not found!"}), 404
    old_product_id = purchase.product_id
    old_quantity = purchase.purchase_quantity
    old_rate = purchase.purchase_rate
    print(old_product_id,'--->>>>>>')
    # Update the Purchase table
    purchase.product_id = data.get('product_id', purchase.product_id)
    purchase.purchase_quantity = data.get('purchase_quantity', purchase.purchase_quantity)
    purchase.purchase_rate = data.get('purchase_rate', purchase.purchase_rate)
    purchase.purchase_amount = purchase.purchase_quantity * purchase.purchase_rate
    purchase.purchase_date = datetime.utcnow()

    db.session.commit()

    # Update the Stock table
    stock = Stock.query.get(purchase.product_id)
    if stock:
        stock.product_quantity += purchase.purchase_quantity - old_quantity
        stock.last_update_date = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Purchase entry updated successfully and stock adjusted!"})

# Delete a purchase entry
@purchase_bp.route('/purchase/<int:id>', methods=['DELETE'])
def delete_purchase(id):
    purchase = Purchase.query.get(id)
    if not purchase:
        return jsonify({"message": "Purchase entry not found!"}), 404

    # Update the Stock table
    stock = Stock.query.get(purchase.product_id)
    if stock:
        stock.product_quantity -= purchase.purchase_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0
        stock.last_update_date = datetime.utcnow()

    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase entry deleted successfully and stock adjusted!"})
