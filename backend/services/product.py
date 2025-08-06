from flask import Blueprint, request, jsonify
from utils.db_helpers import get_all_products, get_product_by_id
from models import Product
from utils.db_helpers import get_session, commit_with_rollback

product_bp = Blueprint("product", __name__)

@product_bp.route("/list", methods=["GET"])
def list_products():
    return jsonify([p.__dict__ for p in get_all_products()])

@product_bp.route("/<int:product_id>", methods=["GET"])
def show_product(product_id):
    product = get_product_by_id(product_id)
    return jsonify(product.__dict__ if product else {"error": "Not found"})

@product_bp.route("/search")
def search_product():
    keyword = request.args.get("q", "").lower()
    session = get_session()
    results = session.query(Product).filter(Product.product_name.ilike(f"%{keyword}%")).all()
    session.close()
    return jsonify([p.__dict__ for p in results])

@product_bp.route("/homepage")
def homepage_products():
    products = get_all_products()[:8]
    return jsonify([p.__dict__ for p in products])
