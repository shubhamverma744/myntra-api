from flask import Blueprint, request, jsonify
from models import Buyer
from utils.db_helpers import create_buyer, get_session, commit_with_rollback

buyer_bp = Blueprint("buyer", __name__)

# ✅ Signup Route
@buyer_bp.route("/signup", methods=["POST"])
def buyer_signup():
    data = request.json
    session = get_session()
    try:
        buyer = Buyer(**data)
        session.add(buyer)
        commit_with_rollback(session)
        session.refresh(buyer)
        return jsonify({"message": "Buyer created", "id": buyer.id})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# ✅ Signin Route
@buyer_bp.route("/signin", methods=["POST"])
def buyer_signin():
    data = request.json
    session = get_session()
    try:
        buyer = session.get(Buyer, data.get("id"))
        if buyer and buyer.password == data.get("password"):
            return jsonify({"message": "Login success", "id": buyer.id})
        return jsonify({"error": "Invalid credentials"}), 401
    finally:
        session.close()
