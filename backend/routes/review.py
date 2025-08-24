from flask import Blueprint, request, jsonify
from models import Review
from utils.db_helpers import get_session

review_bp = Blueprint("review", __name__)

from flask import Blueprint, request, jsonify, session
from models import Review
from utils.db_helpers import get_session

review_bp = Blueprint("review", __name__)

# ✅ Create a new review
@review_bp.route("/add", methods=["POST"])
def create_review():
    db = get_session()

    try:
        # 🔒 Ensure buyer is logged in
        if not session.get("is_authenticated") or not session.get("buyer_id"):
            return jsonify({"error": "Unauthorized. Please log in as buyer."}), 401

        data = request.json

        new_review = Review(
            rating=data["rating"],
            title=data.get("title"),
            content=data.get("content"),
            product_id=data["product_id"],
            buyer_id=session["buyer_id"]   # ✅ take from session, not request
        )

        db.add(new_review)
        db.commit()

        return jsonify({
            "message": "Review created successfully",
            "review_id": new_review.id
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


# # ✅ Get review by ID
# @review_bp.route("/<int:review_id>", methods=["GET"])
# def get_review(review_id):
#     session = get_session()
#     try:
#         review = session.query(Review).get(review_id)
#         if not review:
#             return jsonify({"error": "Review not found"}), 404

#         result = {
#             "id": review.id,
#             "rating": review.rating,
#             "product_id": review.product_id,
#             "buyer_id": review.buyer_id
#         }
#         return jsonify(result)
#     finally:
#         session.close()


# ✅ Get all reviews for a given product
@review_bp.route("/product/<string:product_id>", methods=["GET"])
def get_reviews_by_product(product_id):
    db = get_session()
    try:
        reviews = db.query(Review).filter_by(product_id=product_id).all()
        if not reviews:
            return jsonify({"message": "No reviews found for this product"}), 404

        review_list = []
        for r in reviews:
            review_list.append({
                "id": r.id,
                "rating": r.rating,
                "title": r.title,
                "content": r.content,
                "product_id": r.product_id,
                "buyer_id": r.buyer_id,
                "created_at": r.created_at,
            })

        return jsonify(review_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()
