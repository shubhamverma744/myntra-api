from flask import Blueprint, request, jsonify, session
from utils.db_helpers import get_session, commit_with_rollback
from models.models_all import SubCategory, Product

subcategory_bp = Blueprint("subcategory", __name__, url_prefix="/subcategories")

# Get all subcategories
@subcategory_bp.get("/")
def list_all_subcategories():
    db = get_session()
    try:
        subcategories = db.query(SubCategory).all()
        category_list = []
        for c in subcategories:
            category_list.append({
                "name": c.name,
                "id": c.id
            })
        return jsonify({"categories": category_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# ✅ Get a specific subcategory with its products
@subcategory_bp.get("/<string:subcategory_id>")
def get_subcategory(subcategory_id):
    db = get_session()
    try:
        # Use the class name SubCategory in the query
        subcategory_obj = db.query(SubCategory).filter_by(id=subcategory_id).first()
        if not subcategory_obj:
            return jsonify({"error": "Subcategory not found"}), 404

        # Fetch products under this subcategory
        products = db.query(Product).filter_by(product_sub_category=subcategory_id).all()
        product_list = []
        for p in products:
            product_list.append({
                "product_name": p.product_name,
                "seller_id": p.seller_id,
                "subcategory_id": p.product_sub_category
            })

        subcategory_data = {
            "id": subcategory_obj.id,
            "name": subcategory_obj.name,
        }
        return jsonify({"subcategory": subcategory_data, "products": product_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
        
# ✅ Add subcategory
@subcategory_bp.route("/add", methods=["POST"])
def add_subcategory():
    if not session.get("is_authenticated") or not session.get("seller_id"):
      return jsonify({"error": "Unauthorized. Please log in as seller."}), 401

    db = get_session()
    data = request.json
    try:
        required_fields = [
            "name", "category_id"
        ]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
         return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Set seller_id from session
        # data["seller_id"] = session["seller_id"]

        # ✅ Create and insert product
        subcategory = SubCategory(**data)
        db.add(subcategory)
        commit_with_rollback(db)
        db.refresh(subcategory)

        return jsonify({"message": "subcategory added successfully", "subcategory_id": subcategory.id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
   
# ✅ Get all products under a category
@subcategory_bp.get("/<string:subcategory_id>/products")
def get_products_by_subcategory(subcategory_id):
    db = get_session()
    try:
        products = db.query(Product).filter_by(product_category=subcategory_id).all()
        product_list = []
        for p in products:
            product_list.append({
                "product_name": p.product_name,
                
            })

        return jsonify({"subcategory_id": subcategory_id, "products": product_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# ✅ Add subcategory linked to category
@subcategory_bp.route("/add", methods=["POST"])
def add_sub_category():
    if not session.get("is_authenticated") or not session.get("seller_id"):
        return jsonify({"error": "Unauthorized. Please log in as seller."}), 401

    db = get_session()
    data = request.json
    try:
        # Require name and category_id
        required_fields = ["name", "category_id"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Check if parent category exists
        parent_category = db.query(subcategory).filter_by(id=data["category_id"]).first()
        if not parent_category:
            return jsonify({"error": "Parent category not found"}), 404

        # Create subcategory linked to parent category
        subcategory = subcategory(**data)
        db.add(subcategory)
        commit_with_rollback(db)
        db.refresh(subcategory)

        return jsonify({
            "message": "SubCategory added successfully",
            "sub_category_id": subcategory.id,
            "category_id": subcategory.category_id
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
