from flask import Blueprint, jsonify

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/", methods=["GET"])
def view_cart():
    return jsonify({"message": "Cart details"})
