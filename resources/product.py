from models import Product
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from db import db


product_bp = Blueprint('product_bp', __name__)

# Insert a new product
@product_bp.route('/product', methods=['POST'])
def insert_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        category=data['category'],
        introduce_date=datetime.utcnow()  # or data['introduce_date'] if provided
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

# Update an existing product
@product_bp.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404
    
    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.introduce_date = data.get('introduce_date', product.introduce_date)
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"})

# Delete a product
@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found!"}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})

# Show all products
@product_bp.route('/products', methods=['GET'])
def show_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'introduce_date': product.introduce_date
        }
        output.append(product_data)
    return jsonify(output)

# Show products by category
@product_bp.route('/products/category/<string:category>', methods=['GET'])
def show_products_by_category(category):
    products = Product.query.filter_by(category=category).all()
    if not products:
        return jsonify({"message": "No products found in this category!"}), 404
    
    output = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'introduce_date': product.introduce_date
        }
        output.append(product_data)
    return jsonify(output)
