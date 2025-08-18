from flask import Blueprint
from routes.auth import auth_bp
from routes.cart import cart_bp
from routes.order import order_bp
from routes.product import product_bp
from routes.buyer import buyer_bp
from routes.seller import seller_bp
from routes.root import root_bp
from routes.buyer_address import address_bp
from routes import product
from fastapi import APIRouter


def register_routes(app):
    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(buyer_bp, url_prefix="/buyer")
    app.register_blueprint(seller_bp, url_prefix="/seller")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(cart_bp, url_prefix="/buyer/cart")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(address_bp, url_prefix="/address")



# router = APIRouter()
# router.include_router(product.router)
