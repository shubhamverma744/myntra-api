from flask import Blueprint, jsonify

order_bp = Blueprint("order", __name__)

@order_bp.get("/<int:order_id>")
def get_order(order_id):
    return jsonify({"order_id": order_id})
