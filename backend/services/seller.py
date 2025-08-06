from flask import Blueprint, request, jsonify
from models import Seller
from utils.db_helpers import get_seller_by_id, get_session, commit_with_rollback

seller_bp = Blueprint("seller", __name__)

@seller_bp.route("/signup", methods=["POST"])
def seller_signup():
    data = request.json
    session = get_session()
    seller = Seller(**data)
    session.add(seller)
    commit_with_rollback(session)
    session.refresh(seller)
    session.close()
    return jsonify({"message": "Seller created", "id": seller.id})

@seller_bp.route("/signin", methods=["POST"])
def seller_signin():
    data = request.json
    seller = get_seller_by_id(data.get("id"))
    if seller and seller.password == data.get("password"):
        return jsonify({"message": "Login success", "id": seller.id})
    return jsonify({"error": "Invalid credentials"}), 401

@seller_bp.route("/earnings/<int:seller_id>")
def seller_earnings(seller_id):
    session = get_session()
    from models import Product, OrderItem
    products = session.query(Product.id).filter_by(seller_id=seller_id).all()
    product_ids = [p[0] for p in products]
    items = session.query(OrderItem).filter(OrderItem.product_id.in_(product_ids)).all()
    earning = len(items) * 100  # TODO: use actual price
    session.close()
    return jsonify({"seller_id": seller_id, "estimated_earnings": earning})
