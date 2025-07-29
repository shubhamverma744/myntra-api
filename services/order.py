from flask import Blueprint, request, jsonify
from utils.db_helpers import create_order, get_order_by_id
from models import Order
from utils.db_helpers import get_session

order_bp = Blueprint("order", __name__)

@order_bp.route("/place", methods=["POST"])
def place_order():
    data = request.json
    buyer_id = data.get("buyer_id")
    items = data.get("items", [])
    order = create_order(buyer_id, items)
    return jsonify({"message": "Order placed", "order_id": order.id})

@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = get_order_by_id(order_id)
    return jsonify(order.__dict__ if order else {"error": "Not found"})
