from flask import Blueprint, request, jsonify
from utils.db_helpers import create_buyer, get_buyer_by_id

buyer_bp = Blueprint("buyer", __name__)

@buyer_bp.route("/signup", methods=["POST"])
def buyer_signup():
    data = request.json
    buyer = create_buyer(data)
    return jsonify({"message": "Buyer created", "id": buyer.id})

@buyer_bp.route("/signin", methods=["POST"])
def buyer_signin():
    data = request.json
    buyer = get_buyer_by_id(data.get("id"))
    if buyer and buyer.password == data.get("password"):
        return jsonify({"message": "Login success", "id": buyer.id})
    return jsonify({"error": "Invalid credentials"}), 401
