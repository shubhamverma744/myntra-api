from flask import Blueprint

from services.buyer import buyer_bp
from services.seller import seller_bp
from services.product import product_bp
from services.order import order_bp

def register_routes(app):
    app.register_blueprint(buyer_bp, url_prefix="/buyer")
    app.register_blueprint(seller_bp, url_prefix="/seller")
    app.register_blueprint(product_bp, url_prefix="/product")
    app.register_blueprint(order_bp, url_prefix="/order")

