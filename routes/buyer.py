# from flask import Blueprint, request, jsonify
# from models import Buyer
# from utils.db_helpers import create_buyer, get_session, commit_with_rollback

# buyer_bp = Blueprint("buyer", __name__)

# # ✅ Signup Route
# @buyer_bp.route("/signup", methods=["POST"])
# def buyer_signup():
#     data = request.json
#     session = get_session()
#     try:
#         buyer = Buyer(**data)
#         session.add(buyer)
#         commit_with_rollback(session)
#         session.refresh(buyer)
#         return jsonify({"message": "Buyer created", "id": buyer.id})
#     except Exception as e:
#         session.rollback()
#         return jsonify({"error": str(e)}), 400
#     finally:
#         session.close()

# # ✅ Signin Route
# @buyer_bp.route("/signin", methods=["POST"])
# def buyer_signin():
#     data = request.json
#     session = get_session()
#     try:
#         buyer = session.get(Buyer, data.get("id"))
#         if buyer and buyer.password == data.get("password"):
#             return jsonify({"message": "Login success", "id": buyer.id})
#         return jsonify({"error": "Invalid credentials"}), 401
#     finally:
#         session.close()


from flask import Blueprint, request, jsonify, session
from models import Buyer, Order
from utils import hash_password, verify_password
from utils.db_helpers import get_session, commit_with_rollback
from datetime import datetime

buyer_bp = Blueprint("buyer", __name__)

# ✅ Buyer Signup
@buyer_bp.route("/signup", methods=["POST"])
def buyer_signup():
    data = request.json
    db_session = get_session()
    try:
        # ✅ Required fields
        required_fields = ["username", "password", "email", "phone"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Trim and sanitize input
        username = str(data.get("username")).strip()
        password = str(data.get("password")).strip()
        email = str(data.get("email")).strip()
        phone = str(data.get("phone")).strip()

        # ✅ Validate input
        if len(username) < 3 or len(password) < 6:
            return jsonify({"error": "Username must be 3+ chars and password 6+ chars"}), 400

        buyer_data = {
                "username": username,
                "password": hash_password(password),
                "email": email,
                "phone": phone,
            "since_active": datetime.utcnow()
        }

        buyer = Buyer(**buyer_data)
        db_session.add(buyer)
        commit_with_rollback(db_session)
        db_session.refresh(buyer)

        return jsonify({"message": "Buyer created", "id": buyer.id})

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db_session.close()


# ✅ Buyer Signin
@buyer_bp.route("/signin", methods=["POST"])
def buyer_signin():
    data = request.json
    db_session = get_session()
    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        buyer = db_session.query(Buyer).filter_by(username=username).first()

        if not buyer or not verify_password(password, buyer.password):
            return jsonify({"error": "Invalid credentials"}), 401

        # ✅ Set session
        session["buyer_id"] = buyer.id
        session["username"] = buyer.username
        session["is_authenticated"] = True

        return jsonify({
            "message": "Login success",
            "id": buyer.id,
            "session": {
                "buyer_id": session["buyer_id"],
                "username": session["username"]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ✅ Example Protected Route - Buyer Orders
@buyer_bp.route("/orders", methods=["GET"])
def buyer_orders():
    if not session.get("is_authenticated") or not session.get("buyer_id"):
        return jsonify({"error": "Unauthorized access"}), 401

    buyer_id = session["buyer_id"]
    db_session = get_session()
    try:
        orders = db_session.query(Order).filter_by(buyer_id=buyer_id).all()
        order_list = [{
            "order_id": o.id,
            "status": o.status,
            "created_at": o.created_at.isoformat()
        } for o in orders]

        return jsonify({
            "buyer_id": buyer_id,
            "orders": order_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()
