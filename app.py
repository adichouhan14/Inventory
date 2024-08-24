from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
from models import __init__
from db import db
from flask_migrate import Migrate
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase_bkp import purchase_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost:5432/saheb_stone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(purchase_bp)


migrate = Migrate(app, db)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create tables within the application context
    app.run(debug=True)