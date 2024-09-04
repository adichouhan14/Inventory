from flask import Flask, request, jsonify, render_template
from models import *

from db import db, product_unit
from flask_migrate import Migrate
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase import purchase_bp
from resources.sales import sales_bp
import os
from dotenv import load_dotenv
from resources.product import *
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_url")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration objects
db.init_app(app)
migrate = Migrate(app, db)

# Import Blueprints (assuming you have created these in separate files)
from resources.product import product_bp
from resources.stock import stock_bp
from resources.purchase import purchase_bp
from resources.sales import sales_bp

# Register Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(sales_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create tables within the application context
    app.run(debug=True)