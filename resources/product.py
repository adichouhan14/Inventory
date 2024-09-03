# from models import Product
from models import *
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from db import db
from sqlalchemy import or_

product_bp = Blueprint('product_bp', __name__)

# Get product by ID
@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'category': product.category.name,  # Assuming relationship with Category
            'introduce_date': product.introduce_date.strftime('%Y-%m-%d')
        })
    else:
        return jsonify({'error': 'Product not found'}), 404

# Insert a new product
@product_bp.route('/product', methods=['POST'])
def insert_product():
    try:
        data = request.json
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            return jsonify({"message": "Category not found!"}), 404

        new_product = Product(
            name=data['name'],
            category=category,
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
    data = request.json
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404

    category = Category.query.filter_by(name=data.get('category', product.category.name)).first()
    if not category:
        return jsonify({"message": "Category not found!"}), 404

    product.name = data.get('name', product.name)
    product.category = category
    product.introduce_date = data.get('introduce_date', product.introduce_date)

    db.session.commit()
    return jsonify({"message": "Product updated successfully!"}), 200

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
