from flask import Blueprint, request, jsonify
from models import CartItem, Product
from utils.db_helpers import get_session, commit_with_rollback

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json
    buyer_id = data.get("buyer_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not all([buyer_id, product_id]):
        return jsonify({"error": "buyer_id and product_id are required"}), 400

    session = get_session()
    try:
        # Check if product exists
        product = session.get(Product, product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Check if item already in cart
        cart_item = session.query(CartItem).filter_by(buyer_id=buyer_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(buyer_id=buyer_id, product_id=product_id, quantity=quantity)
            session.add(cart_item)

        commit_with_rollback(session)
        return jsonify({"message": "Item added to cart"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
