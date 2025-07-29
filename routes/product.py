from flask import Blueprint, jsonify

product_bp = Blueprint("product", __name__)

@product_bp.get("/")
def list_all_products():
    return jsonify({"products": []})

@product_bp.get("/<int:product_id>")
def get_product(product_id):
    return jsonify({"product": {"id": product_id}})
