from flask import Blueprint, jsonify, request, render_template
from db import db
from models import Purchase, Stock, Product
from datetime import datetime
import traceback
from sqlalchemy import or_

# Create a Blueprint
purchase_bp = Blueprint('purchase_bp', __name__)


# Insert a new purchase entry
@purchase_bp.route('/purchase', methods=['POST'])
def insert_purchase():
    try:
        # data = request.form
        data = request.get_json()

        # Check if 'product_id' exists in the data
        if 'product_id' not in data:
            return jsonify({'error': 'product_id is missing'}), 400
        
        print('data-->', data)
        product_id = data['product_id']
        purchase_quantity = float(data['purchase_quantity'])
        purchase_rate = float(data['purchase_rate'])
        purchase_amount = round(purchase_quantity * purchase_rate,2)
        purchase_date = datetime.strptime(data['add_purchase_date'], '%Y-%m-%d') 
        # Optional supplier details
        supplier_name = data.get('supplier_name', None)
        supplier_contact = data.get('supplier_contact', None)
        supplier_address = data.get('supplier_address', None)

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
            purchase_date=purchase_date,
            supplier_name=supplier_name,
            supplier_contact=supplier_contact,
            supplier_address=supplier_address
        )
        db.session.add(new_purchase)

        # Update the Stock table
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
        traceback.print_exc()
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
    products = Product.query.all()
    return render_template('purchases.html', purchases=purchases,products=products, pagination=pagination)

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
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d'),
            'supplier_name': purchase.supplier_name,
            'supplier_contact': purchase.supplier_contact,
            'supplier_address': purchase.supplier_address
        }
        return jsonify(purchase_data), 200

    # Handle the PUT method for updating the purchase entry
    data = request.get_json()
    purchase = Purchase.query.get(id)
    print('update purchase data--->', data, '--->>', purchase, request)

    if not purchase:
        return jsonify({"message": "Purchase entry not found!"}), 404

    old_quantity = purchase.purchase_quantity
    old_product_id = purchase.product_id

    # Update the Purchase table
    purchase.product_id = data.get('product_id', purchase.product_id)
    purchase.purchase_quantity = data.get('purchase_quantity', purchase.purchase_quantity)
    purchase.purchase_rate = data.get('purchase_rate', purchase.purchase_rate)
    purchase.purchase_amount = round(float(purchase.purchase_quantity) * float(purchase.purchase_rate),2)
    purchase.purchase_date = datetime.utcnow()

    # Update optional supplier details
    purchase.supplier_name = data.get('supplier_name', purchase.supplier_name)
    purchase.supplier_contact = data.get('supplier_contact', purchase.supplier_contact)
    purchase.supplier_address = data.get('supplier_address', purchase.supplier_address)

    # Adjust the Stock for the old product
    if old_product_id != purchase.product_id:
        old_stock = Stock.query.filter_by(product_id=old_product_id).first()
        if old_stock:
            old_stock.product_quantity -= old_quantity
            if old_stock.product_quantity < 0:
                old_stock.product_quantity = 0  # Prevent negative stock quantities
            old_stock.last_update_date = datetime.utcnow()

    # Adjust the Stock for the new product
    new_stock = Stock.query.filter_by(product_id=purchase.product_id).first()
    if new_stock:
        new_stock.product_quantity += float(purchase.purchase_quantity)
        if new_stock.product_quantity < 0:
            new_stock.product_quantity = 0  # Prevent negative stock quantities
        new_stock.last_update_date = datetime.utcnow()
    else:
        # If no stock entry exists for the new product, create one
        new_stock = Stock(
            product_id=purchase.product_id,
            product_quantity=purchase.purchase_quantity,
            last_update_date=datetime.utcnow()
        )
        db.session.add(new_stock)

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
        filtered_purchases = Purchase.query.join(Product).filter(
            or_(Product.name.ilike(f'%{query}%'),
                Purchase.supplier_name.ilike(f'%{query}%')
                )
            ).all()

    # Convert the filtered purchases to a list of dictionaries for JSON response
    purchase_list = [{
            'id': purchase.id,
            'name': purchase.product.name,
            'purchase_quantity': purchase.purchase_quantity,
            'purchase_rate': purchase.purchase_rate,
            'purchase_amount': purchase.purchase_amount,
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d'),
            'supplier_name': purchase.supplier_name,
            'supplier_contact': purchase.supplier_contact,
            'supplier_address': purchase.supplier_address
        } for purchase in filtered_purchases]

    return jsonify(purchases=purchase_list)