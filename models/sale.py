from datetime import datetime
from db import db
# Sales Table
class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    sales_quantity = db.Column(db.Integer, nullable=False)
    sales_rate = db.Column(db.Float, nullable=False)
    sales_amount = db.Column(db.Float, nullable=False)
    sales_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
    
    def __repr__(self):
        return f"<Sale Product ID {self.product_id} - Quantity {self.sales_quantity}>"