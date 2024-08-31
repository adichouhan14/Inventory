from flask import Blueprint, jsonify, request, render_template, url_for
from db import db
from models import Sale, Stock, Product
from datetime import datetime

# Create a Blueprint
sales_bp = Blueprint('sales_bp', __name__)


# Insert a new sale entry
@sales_bp.route('/sale', methods=['POST'])
def insert_sale():
    try:
        data = request.form
        print('data-->', data)
        product_id = data['product_id']
        sales_quantity = int(data['sales_quantity'])
        sales_rate = float(data['sales_rate'])
        sales_amount = sales_quantity * sales_rate

        # Check if the product exists in the Product table
        product = Product.query.get(product_id)
        if not product:
            print('Product not found in Product table!')
            return jsonify({"message": "Product not found in Product table!"}), 404

        # Check if the stock exists and if there is enough stock available
        # stock = Stock.query.get(product_id)
        stock = db.session.query(Stock).filter(Stock.product_id == product_id).first()
        if not stock:
            return jsonify({"message": "Stock entry not found for the product!"}), 404
        if stock.product_quantity < sales_quantity:
            return jsonify({"message": "Insufficient stock available!"}), 400

        # Insert into Sale table
        new_sale = Sale(
            product_id=product_id,
            sales_quantity=sales_quantity,
            sales_rate=sales_rate,
            sales_amount=sales_amount,
            sales_date=datetime.utcnow()
        )
        db.session.add(new_sale)

        # Update the Stock table
        stock.product_quantity -= sales_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0  # Prevent negative stock quantities
        stock.last_update_date = datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Sale entry added successfully and stock updated!"}), 201
    except Exception as e:
        print('Exception in sales-->', e)
        return jsonify({"message": "Failed to insert sales."}), 500

# Show all sale entries
@sales_bp.route('/sales', methods=['GET'])
def show_sales():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Sale.query.paginate(page=page, per_page=per_page, error_out=False)
    sales = pagination.items
    for sale in sales:
        sale.name = sale.product.name
    return render_template('sales.html', sales=sales, pagination=pagination)

# Retrieve sale data for editing
@sales_bp.route('/sale/<int:id>', methods=['GET', 'PUT'])
def update_sale(id):
    if request.method == 'GET':
        sale = Sale.query.get(id)
        if not sale:
            return jsonify({"message": "Sale entry not found!"}), 404

        sale_data = {
            'id': sale.id,
            'product_id': sale.product_id,
            'name': sale.product.name,
            'sales_quantity': sale.sales_quantity,
            'sales_rate': sale.sales_rate,
            'sales_amount': sale.sales_amount,
            'sales_date': sale.sales_date.strftime('%Y-%m-%d')
        }
        return jsonify(sale_data), 200

    # Continue with the PUT method as already defined
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
    sale.sales_amount = int(sale.sales_quantity) * float(sale.sales_rate)
    sale.sales_date = datetime.utcnow()

    db.session.commit()

    # Update the Stock table
    stock = Stock.query.filter_by(product_id=sale.product_id).first()
    if stock:
        stock.product_quantity += old_quantity - sale.sales_quantity
        if stock.product_quantity < 0:
            stock.product_quantity = 0  # Prevent negative stock quantities
        stock.last_update_date = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Sale entry updated successfully and stock adjusted!"}), 200

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
    return jsonify({"message": "Sale entry deleted successfully and stock adjusted!"}), 200

#Filter sales
@sales_bp.route('/sale/filter')
def filter_sale():
    print('In sales filter')
    query = request.args.get('query', '', type=str).strip()

    # Separate query by ID if it's numeric
    if query.isdigit():
        filtered_sales = Sale.query.filter(Sale.id == int(query)).all()
        print('filtered_sales id-->', filtered_sales)
    else:
        
        filtered_sales = Sale.query.join(Product).filter(Product.name.ilike(f'%{query}%')).all()
        # filtered_sales = Sale.query.join(Product).filter(Product.name.ilike(f'%{query}%')).all()
        print('filtered_sales-->', filtered_sales)
        

    sales_list = [{
        'id': sale.id,
        'name': sale.product.name,
        'sales_quantity': sale.sales_quantity,
        'sales_rate': sale.sales_rate,
        'sales_amount': sale.sales_amount,
        'sales_date': sale.sales_date.strftime('%Y-%m-%d')
    } for sale in filtered_sales]
    print('sales_list-->',sales_list)
    return jsonify(sales=sales_list)