# routes/root.py

from flask import Blueprint, jsonify

root_bp = Blueprint("root", __name__)

@root_bp.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Welcome to the Myntra Clone API 🎉",
        "status": "running"
    }), 200
