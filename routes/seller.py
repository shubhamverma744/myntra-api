from flask import Blueprint, request, jsonify, session
from models import Seller, Product, OrderItem
from utils.db_helpers import get_seller_by_id, get_session, commit_with_rollback
from utils import hash_password, verify_password
from datetime import datetime


seller_bp = Blueprint("seller", __name__)

# ✅ Seller Signup
@seller_bp.route("/signup", methods=["POST"])
def seller_signup():
    data = request.json
    session = get_session()
    try:
        # ✅ Required Fields
        required_fields = ["username", "password", "official_name", "address"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Trim and sanitize strings
        username = str(data.get("username")).strip()
        password = str(data.get("password")).strip()
        official_name = str(data.get("official_name")).strip()
        address = str(data.get("address")).strip()

        # ✅ Basic length validations
        if len(username) < 3 or len(password) < 6:
            return jsonify({"error": "Username must be 3+ chars and password 6+ chars"}), 400

        # ✅ Construct seller data
        seller_data = {
            "username": username,
            "password": hash_password(password),
            "official_name": official_name,
            "address": address,
            "kyc": False,
            "seller_rating": None,
            "since_active": datetime.utcnow()
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

@seller_bp.route("/signin", methods=["POST"])
def seller_signin():
    data = request.json
    db_session = get_session()
    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        seller = db_session.query(Seller).filter_by(username=username).first()

        if not seller or not verify_password(password, seller.password):
            return jsonify({"error": "Invalid credentials"}), 401

        # ✅ Set Flask session
        session["seller_id"] = seller.id
        session["username"] = seller.username
        session["is_authenticated"] = True

        return jsonify({
            "message": "Login success",
            "id": seller.id,
            "session": {
                "seller_id": session["seller_id"],
                "username": session["username"]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

      
# ✅ Seller Earnings (using session)
@seller_bp.route("/earnings", methods=["GET"])
def seller_earnings():
    if not session.get("is_authenticated") or not session.get("seller_id"):
        return jsonify({"error": "Unauthorized access"}), 401

    seller_id = session["seller_id"]
    db_session = get_session()
    try:
        # Get all product IDs for this seller
        products = db_session.query(Product.id).filter_by(seller_id=seller_id).all()
        product_ids = [p[0] for p in products]

        # Get all order items for these products
        items = db_session.query(OrderItem).filter(OrderItem.product_id.in_(product_ids)).all()

        # ✅ Calculate earnings (replace with item.price if available)
        earnings = sum([100 for _ in items])  # Placeholder per item

        return jsonify({
            "seller_id": seller_id,
            "estimated_earnings": earnings,
            "products_sold": len(items)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

