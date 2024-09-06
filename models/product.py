# models/product.py
from datetime import datetime
from db import db
from .category import Category

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unit = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    introduce_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to access category details
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    
    def __repr__(self):
        return f"<Product {self.name} - {self.category.name}>"
