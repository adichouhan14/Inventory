from flask import Blueprint, jsonify, request, render_template
from db import db
from models import Purchase, Stock, Product
from datetime import datetime

# Create a Blueprint
purchase_bp = Blueprint('purchase_bp', __name__)


# Insert a new purchase entry
@purchase_bp.route('/purchase', methods=['POST'])
def insert_purchase():
    try:
        data = request.form
        product_id = data['product_id']
        purchase_quantity = int(data['purchase_quantity'])
        purchase_rate = float(data['purchase_rate'])
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
        # Update the Stock tablea
        stock = db.session.query(Stock).filter(Stock.product_id == product_id).first()
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
    except Exception as e:
        print('Exception in purchase-->', e)
        return jsonify({"message": "Failed to insert purchase."}), 500

# Show all purchase entries
@purchase_bp.route('/purchases', methods=['GET'])
def show_purchases():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Purchase.query.paginate(page=page, per_page=per_page, error_out=False)
    purchases = pagination.items
    for purchase in purchases:
        purchase.name = purchase.product.name
    return render_template('purchases.html', purchases=purchases, pagination=pagination)

# Retrieve purchase data for editing
@purchase_bp.route('/purchase/<int:id>', methods=['GET', 'PUT'])
def update_purchase(id):
    if request.method == 'GET':
        purchase = Purchase.query.get(id)
        if not purchase:
            return jsonify({"message": "Purchase entry not found!"}), 404

        purchase_data = {
            'id': purchase.id,
            'product_id': purchase.product_id,
            'name': purchase.product.name,
            'purchase_quantity': purchase.purchase_quantity,
            'purchase_rate': purchase.purchase_rate,
            'purchase_amount': purchase.purchase_amount,
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d')
        }
        return jsonify(purchase_data), 200

    # Handle the PUT method for updating the purchase entry
    data = request.get_json()
    purchase = Purchase.query.get(id)
    if not purchase:
        return jsonify({"message": "Purchase entry not found!"}), 404

    old_quantity = purchase.purchase_quantity
    old_rate = purchase.purchase_rate

    # Update the Purchase table
    purchase.product_id = data.get('product_id', purchase.product_id)
    purchase.purchase_quantity = data.get('purchase_quantity', purchase.purchase_quantity)
    purchase.purchase_rate = data.get('purchase_rate', purchase.purchase_rate)
    purchase.purchase_amount = int(purchase.purchase_quantity) * float(purchase.purchase_rate)
    purchase.purchase_date = datetime.utcnow()

    db.session.commit()

    # Update the Stock table
    stock = Stock.query.filter_by(product_id=purchase.product_id).first()
    if stock:
        stock.product_quantity += purchase.purchase_quantity - old_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0  # Prevent negative stock quantities
        stock.last_update_date = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Purchase entry updated successfully and stock adjusted!"}), 200

# Delete a purchase entry
@purchase_bp.route('/purchase/<int:id>', methods=['DELETE'])
def delete_purchase(id):
    print('delete_purchase-->',id)
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

#Fliter purchase
@purchase_bp.route('/purchase/filter')
def filter_purchase():
    print('Inside purchase filter')
    query = request.args.get('query', '', type=str).strip()

    # If the query is numeric, treat it as an ID
    if query.isdigit():
        filtered_purchases = Purchase.query.filter(Purchase.id == int(query)).all()
    else:
        # Filter by product name
        # filtered_purchases = Purchase.query.join(Product).filter(
        #     (Purchase.product_id == Product.id) & 
        #     ((Product.name.ilike(f'%{query}%')) | (Purchase.id == query))
        # ).all()
        filtered_purchases = Purchase.query.join(Product).filter(Product.name.ilike(f'%{query}%')).all()

    # Convert the filtered purchases to a list of dictionaries for JSON response
    purchase_list = [{
            'id': purchase.id,
            'name': purchase.product.name,
            'purchase_quantity': purchase.purchase_quantity,
            'purchase_rate': purchase.purchase_rate,
            'purchase_amount': purchase.purchase_amount,
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d'),
        } for purchase in filtered_purchases]

    return jsonify(purchases=purchase_list)