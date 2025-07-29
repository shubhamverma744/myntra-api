from flask import Blueprint, request, jsonify
from models import Seller, Product, OrderItem
from utils.db_helpers import get_seller_by_id, get_session, commit_with_rollback
from utils import hash_password
from datetime import datetime


seller_bp = Blueprint("seller", __name__)

# ✅ Seller Signup
@seller_bp.route("/signup", methods=["POST"])
def seller_signup():
    data = request.json
    session = get_session()
    try:
        password = data.get("password")
        seller_data = {
            "username": data.get("username"),
            "password": hash_password(password),
            "official_name": data.get("official_name"),
            "address": data.get("address"),
            "kyc": False,  # Default value
            "seller_rating": None,  # Nullable
            "since_active": datetime.utcnow()  # Current time
        }
        seller = Seller(**seller_data)
        session.add(seller)
        commit_with_rollback(session)
        session.refresh(seller)
        return jsonify({"message": "Seller created", "id": seller.id})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# ✅ Seller Signin
@seller_bp.route("/signin", methods=["POST"])
def seller_signin():
    data = request.json
    session = get_session()
    try:
        seller = get_seller_by_id(data.get("id"))
        if seller and seller.password == data.get("password"):
            return jsonify({"message": "Login success", "id": seller.id})
        return jsonify({"error": "Invalid credentials"}), 401
    finally:
        session.close()

# ✅ Seller Earnings
@seller_bp.route("/earnings/<int:seller_id>")
def seller_earnings(seller_id):
    session = get_session()
    try:
        products = session.query(Product.id).filter_by(seller_id=seller_id).all()
        product_ids = [p[0] for p in products]
        items = session.query(OrderItem).filter(OrderItem.product_id.in_(product_ids)).all()
        earnings = sum([100 for _ in items])  # Placeholder for actual price
        return jsonify({"seller_id": seller_id, "estimated_earnings": earnings})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
