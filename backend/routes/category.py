from flask import Blueprint, request, jsonify, session
from utils.db_helpers import get_session, commit_with_rollback
from models.models_all import Category, Product
import pdb

category_bp = Blueprint("category", __name__, url_prefix="/categories")

# ✅ Get all categories
@category_bp.get("/")
def list_all_categories():
    db = get_session()
    try:
        categories = db.query(Category).all()
        category_list = []
        for c in categories:
            category_list.append({
                "name": c.name,
                "id": c.id
            })
        return jsonify({"categories": category_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ✅ Get a specific category with its products
@category_bp.get("/<string:category_id>")
def get_category(category_id):
    db = get_session()
    try:
        category = db.query(Category).filter_by(id=category_id).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404

        # Fetch products under this category
        products = db.query(Product).filter_by(product_category=category_id).all()
        product_list = []
        for p in products:
            product_list.append({
                "product_name": p.product_name,
                "id": p.seller_id,
                "category_id": p.category_id
               
            })

        category_data = {
            "name": category.name,
        }
        return jsonify({"category": category_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ✅ Add category
@category_bp.route("/add", methods=["POST"])
def add_category():
    if not session.get("is_authenticated") or not session.get("seller_id"):
      return jsonify({"error": "Unauthorized. Please log in as seller."}), 401

    db = get_session()
    data = request.json
    try:
        required_fields = [
            "name"
        ]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
         return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Set seller_id from session
        # data["seller_id"] = session["seller_id"]

        # ✅ Create and insert product
        category = Category(**data)
        db.add(category)
        commit_with_rollback(db)
        db.refresh(category)

        return jsonify({"message": "Category added successfully", "category_id": category.id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
   

# ✅ Get all products under a category
@category_bp.get("/products")
def get_products_by_category():
    db = get_session()
    category_name = request.args.get("category_name")
    try:
        category = db.query(Category).filter_by(name=category_name).first()
        products = db.query(Product).filter_by(category_id=category.id).all()
        product_list = []
        for p in products:
            product_dict = {c.name: getattr(p, c.name) for c in p.__table__.columns}
            product_dict["category_name"] = category.name  # extra field if you want
            product_list.append(product_dict)

        return jsonify({"category_name": category.name, "products": product_list})
    except Exception as e:
        print("🔥 Exception:", e)
        return jsonify({"error": repr(e)}), 500
    finally:
        db.close()
