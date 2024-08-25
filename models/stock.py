from datetime import datetime
from db import db
# Stock Table
class Stock(db.Model):
    __tablename__ = 'stock'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    last_update_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref=db.backref('stocks', lazy=True))
    
    def __repr__(self):
        return f"<Stock Product ID {self.product_id} - Quantity {self.product_quantity}>"