from flask import Blueprint, request, jsonify, session
from models import Product
from utils.db_helpers import get_session, commit_with_rollback

product_bp = Blueprint("product", __name__)

# ✅ Get all products
@product_bp.get("/")
def list_all_products():
    db = get_session()
    try:
        products = db.query(Product).all()
        product_list = []
        for p in products:
            product_list.append({
                "id": p.id,
                "product_name": p.product_name,
                "product_code": p.product_code,
                "brand": p.brand,
                "mrp": p.mrp,
                "selling_price": p.selling_price,
                "stock_quantity": p.stock_quantity,
                "main_image_url": p.main_image_url,
                "seller_id": p.seller_id,
                "category_id": p.category_id
                # Add more fields as needed
            })
        return jsonify({"products": product_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# ✅ Get a specific product
@product_bp.get("/<string:product_id>")
def get_product(product_id):
    db = get_session()
    try:
        product = db.query(Product).filter_by(id=product_id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        product_data = {
            "id": product.id,
            "product_name": product.product_name,
            "product_code": product.product_code,
            "brand": product.brand,
            "product_type": product.product_type,
            "product_category": product.product_category,
            "mrp": product.mrp,
            "selling_price": product.selling_price,
            "discount": product.discount,
            "stock_quantity": product.stock_quantity,
            "gender": product.gender,
            "main_image_url": product.main_image_url,
            "additional_image_urls": product.additional_image_urls,
            "video_url": product.video_url,
            "returnable": product.returnable,
            "return_days": product.return_days,
            "exchange_available": product.exchange_available,
            "seller_id": product.seller_id,
            "category_id": product.category_id
            # Add any other fields you want
        }
        return jsonify({"product": product_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@product_bp.route("/add", methods=["POST"])
def add_product():
    if not session.get("is_authenticated") or not session.get("seller_id"):
        return jsonify({"error": "Unauthorized. Please log in as seller."}), 401

    db = get_session()
    data = request.json
    try:
        required_fields = [
            "product_name", "product_code", "product_type", "product_category",
            "brand", "mrp", "selling_price", "stock_quantity"
        ]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # ✅ Set seller_id from session
        data["seller_id"] = session["seller_id"]

        # ✅ Create and insert product
        product = Product(**data)
        db.add(product)
        commit_with_rollback(db)
        db.refresh(product)

        return jsonify({"message": "Product added successfully", "product_id": product.id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
