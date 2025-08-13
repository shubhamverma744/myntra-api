from flask import Blueprint, request, jsonify, session
from models import Seller, Product, OrderItem
from utils.db_helpers import get_seller_by_id, get_session, commit_with_rollback
from utils import hash_password, verify_password
from datetime import datetime


seller_bp = Blueprint("seller", __name__)

@seller_bp.route("/signup", methods=["POST"])
def seller_signup():
    data = request.json
    session = get_session()
    try:
        # ✅ Required Fields based on Seller model
        required_fields = ["username", "password", "official_name", "email"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Trim and sanitize strings
        username = str(data.get("username")).strip()
        password = str(data.get("password")).strip()
        official_name = str(data.get("official_name")).strip()
        email = str(data.get("email")).strip().lower()
        phone = str(data.get("phone")).strip() if data.get("phone") else None

        # ✅ Basic length validations
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        # ✅ Email format validation (simple check)
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # ✅ Uniqueness checks
        if session.query(Seller).filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 400
        if session.query(Seller).filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        if phone and session.query(Seller).filter_by(phone=phone).first():
            return jsonify({"error": "Phone number already registered"}), 400

        # ✅ Construct seller data (KYC is string — default None)
        seller_data = {
            "username": username,
            "password": hash_password(password),
            "official_name": official_name,
            "email": email,
            "phone": phone,
            "kyc": None,
            "seller_rating": None,
            "since_active": datetime.utcnow().date(),
            "is_active": True,
            "is_verified": False
        }

        # ✅ Create and save seller
        seller = Seller(**seller_data)
        session.add(seller)
        commit_with_rollback(session)
        session.refresh(seller)

        return jsonify({"message": "Seller created successfully", "id": seller.id}), 201

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
        
        
# def payment_details();


