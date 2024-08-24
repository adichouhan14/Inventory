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
    db.session.commit()

    # Create a new entry in Stock table corresponding to this purchase
    new_stock = Stock(
        product_id=product_id,
        product_quantity=purchase_quantity,
        last_purchase_rate=purchase_rate,
        last_update_date=datetime.utcnow()
    )
    db.session.add(new_stock)
    db.session.commit()

    return jsonify({"message": "Purchase entry added successfully and new stock entry created!"}), 201

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
    print('purchase------------>',purchase)
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

    # Find the corresponding Stock entry
    stock = Stock.query.filter_by(product_id=old_product_id, last_purchase_rate=old_rate, product_quantity=old_quantity).first()
    if stock:
        stock.product_id = purchase.product_id
        stock.product_quantity = purchase.purchase_quantity
        stock.last_purchase_rate = purchase.purchase_rate
        stock.last_update_date = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Purchase entry and corresponding stock updated successfully!"})
    else:
        return jsonify({"message": "Corresponding stock entry not found!"}), 404

# Delete a purchase entry
@purchase_bp.route('/purchase/<int:id>', methods=['DELETE'])
def delete_purchase(id):
    purchase = Purchase.query.get(id)
    if not purchase:
        return jsonify({"message": "Purchase entry not found!"}), 404

    # Find the corresponding Stock entry
    stock = Stock.query.filter_by(product_id=purchase.product_id, last_purchase_rate=purchase.purchase_rate, product_quantity=purchase.purchase_quantity).first()
    if stock:
        db.session.delete(stock)

    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase entry and corresponding stock deleted successfully!"})
