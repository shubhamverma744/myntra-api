from flask import Blueprint, request, jsonify, session
from utils.db_helpers import get_session
from models import Order, Product, CartItem
from datetime import datetime

order_bp = Blueprint("order", __name__)

# 🔐 Helper: require login
def require_login():
    buyer_id = session.get("buyer_id")
    if not buyer_id:
        return None, jsonify({"error": "Unauthorized: Please login first"}), 401
    return buyer_id, None, None


# ✅ Get order by ID (only for logged-in buyer)
@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    buyer_id, error_response, status = require_login()
    if error_response:
        return error_response, status

    db = get_session()
    try:
        order = db.query(Order).filter_by(id=order_id, buyer_id=buyer_id).first()
        if not order:
            return jsonify({"error": "Order not found or unauthorized"}), 404

        return jsonify({
            "order_id": order.id,
            "buyer_id": order.buyer_id,
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    finally:
        db.close()


# 🛒 Place a new order (only for logged-in buyer)
@order_bp.route("/place", methods=["POST"])
def place_order():
    buyer_id, error_response, status = require_login()
    if error_response:
        return error_response, status

    data = request.json
    product_ids = data.get("product_ids", [])  # example list of product IDs
    db = get_session()

    try:
        if not product_ids:
            return jsonify({"error": "No products provided"}), 400

        # You can add logic to check stock or get prices
        new_order = Order(
            buyer_id=buyer_id,
            status="placed",
            created_at=datetime.utcnow()
        )
        db.add(new_order)
        db.flush()  # get new_order.id

        # You can use OrderItem or CartItem table if needed
        for product_id in product_ids:
            cart_item = CartItem(
                id=id,
                order_id=new_order.id,
                product_id=product_id,
                quantity=1  # default
            )
            db.add(cart_item)

        db.commit()
        return jsonify({"message": "Order placed", "order_id": new_order.id})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
