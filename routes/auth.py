from flask import Blueprint, request, jsonify
from utils import create_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    # dummy login for buyer/seller
    user_type = request.json.get("type")
    return jsonify({"token": create_token({"role": user_type})})
