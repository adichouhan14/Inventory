# from models import Product
from models import *
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint, render_template
from db import db, product_unit
from sqlalchemy import or_

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products',  methods=['GET'])
def product():
    # products = Product.query.all()  #Fetch all products from the database
    # return render_template('product.html', products=products)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    products = pagination.items
    categories = Category.query.all()
    print('categories called from get product end point',categories)
    return render_template('product.html', categories=categories, products=products, product_unit=product_unit, pagination=pagination)

# Get product by ID
@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    print('get product -->>',product)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'category_id' : product.category_id,
            'category': product.category.name,  # Assuming relationship with Category
            'unit': product.unit,
            'unit_text': product_unit[product.unit],
            'introduce_date': product.introduce_date.strftime('%Y-%m-%d')
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

# Insert a new product
@product_bp.route('/product', methods=['POST'])
def insert_product():
    try:
        print('request post product',request)
        data = request.form
        #category = Category.query.filter_by(name=data['category']).first()
        # if not category:
        #     return jsonify({"message": "Category not found!"}), 404
        print('calling post product data:',data)
        new_product = Product(
            name=data['name'],
            category_id=data['category_id'],
            unit = 1,
            introduce_date=datetime.utcnow()  # or data['introduce_date'] if provided
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        print('Exception occurred while adding product:', e)
        if 'already exists' in str(e):
            return jsonify({"message": "Product already exists."}), 409
        return jsonify({"message": "Failed to insert product."}), 500

# Update an existing product
@product_bp.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()
        product = Product.query.get(id)
        print('put product data',data)
        print('put product',product,product.unit)
        product.name = data.get('name', product.name)
        product.category_id = data.get('category_id',product.category_id) 
        product.unit = int(data.get('recordUnit',product.unit))
        product.introduce_date = data.get('introduce_date', product.introduce_date)

        db.session.commit()
        return jsonify({"message": "Product updated successfully!"}), 200
    
    except Exception as e:
        # Print traceback details in case of an error
        #traceback.print_exc()
        print('Exception:::',e)
        return jsonify({"message": "An error occurred while updating the product entry.", "details": str(e)}), 500
    

# Delete a product
@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"}), 200

# Show products by category
@product_bp.route('/products/category/<string:category>', methods=['GET'])
def show_products_by_category(category):
    category_obj = Category.query.filter_by(name=category).first()
    if not category_obj:
        return jsonify({"message": "Category not found!"}), 404

    products = Product.query.filter_by(category=category_obj).all()
    if not products:
        return jsonify({"message": "No products found in this category!"}), 404

    output = [{
        'id': product.id,
        'name': product.name,
        'category': product.category.name,
        'introduce_date': product.introduce_date.strftime('%Y-%m-%d')
    } for product in products]
    
    return jsonify(output)

# Filter products by name or category
@product_bp.route('/product/filter', methods=['GET'])
def filter_products():
    query = request.args.get('query', '', type=str).strip()
    if query.isdigit():
        filtered_products = Product.query.filter(Product.id == int(query)).all()
        print('filtered_product id-->', filtered_products)
    else:
        filtered_products = Product.query.join(Category).filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Category.name.ilike(f'%{query}%')
            )
        ).all()

    if not filtered_products:
        return jsonify({"message": "No products match the filter criteria."}), 404

    products_list = [{
        'id': product.id,
        'name': product.name,
        'category': product.category.name,
        'introduce_date': product.introduce_date.strftime('%Y-%m-%d')
    } for product in filtered_products]

    return jsonify(products=products_list)

# Show categories
@product_bp.route('/products/category/', methods=['GET'])
def get_category():
    categories = Category.query.all()  # Fetch all categories
    if not categories:
        return jsonify({"message": "No categories found!"}), 404

    category_list = []
    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name
        }
        category_list.append(category_data)

    return jsonify(category_list), 200
