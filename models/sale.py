from datetime import datetime
from db import db

# Sales Table
class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    sales_quantity = db.Column(db.Float, nullable=False)
    sales_rate = db.Column(db.Float, nullable=False)
    sales_amount = db.Column(db.Float, nullable=False)
    sales_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # New columns for customer details
    customer_name = db.Column(db.String(100), nullable=True)
    contact_no = db.Column(db.String(20), nullable=True)
    customer_address = db.Column(db.String(200), nullable=True)
    
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
    
    def __repr__(self):
        return (f"<Sale Sales ID {self.id}, Quantity {self.sales_quantity}, product_id {self.product_id}, "
                f"sales_rate {self.sales_rate}, amount {self.sales_amount}, sales_date {self.sales_date}, "
                f"customer_name {self.customer_name}, contact_no {self.contact_no}, customer_address {self.customer_address}>")
