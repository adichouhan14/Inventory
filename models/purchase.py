# models/purchase.py

from datetime import datetime
from db import db

# Purchase Table
class Purchase(db.Model):
    __tablename__ = 'purchase'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    purchase_quantity = db.Column(db.Float, nullable=False)
    purchase_rate = db.Column(db.Float, nullable=False)
    purchase_amount = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # New Supplier details fields
    supplier_name = db.Column(db.String(100), nullable=True)
    supplier_contact = db.Column(db.String(100), nullable=True)
    supplier_address = db.Column(db.String(255), nullable=True)
    
    product = db.relationship('Product', backref=db.backref('purchases', lazy=True))
    
    def __repr__(self):
        return f"<Purchase Product ID {self.product_id} - Quantity {self.purchase_quantity}>"
