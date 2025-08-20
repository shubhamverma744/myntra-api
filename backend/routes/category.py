from flask import Blueprint, request, jsonify
from utils.db_helpers import get_session, commit_with_rollback
from models.models_all import Category, SubCategory

category_bp = Blueprint("category", __name__, url_prefix="/categories")

# ---------------- Get all categories ----------------
@category_bp.route("/", methods=["GET"])
def get_categories():
    with get_session() as session:
        categories = session.query(Category).all()
        data = []
        for cat in categories:
            data.append({
                "id": cat.id,
                "name": cat.name,
                "subcategories": [{"id": sub.id, "name": sub.name} for sub in cat.subcategories]
            })
        return jsonify(data)


# ---------------- Add new category ----------------
@category_bp.route("/", methods=["POST"])
def add_category():
    data = request.json
    new_cat = Category(name=data["name"])

    with get_session() as session:
        session.add(new_cat)
        commit_with_rollback(session)

    return jsonify({"message": "Category added", "id": new_cat.id})


# ---------------- Add new subcategory ----------------
@category_bp.route("/<category_id>/subcategories", methods=["POST"])
def add_subcategory(category_id):
    data = request.json

    with get_session() as session:
        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        new_sub = SubCategory(name=data["name"], category=category)
        session.add(new_sub)
        commit_with_rollback(session)

        return jsonify({"message": "Subcategory added", "id": new_sub.id})
