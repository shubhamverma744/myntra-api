from flask import Blueprint, request, jsonify
from models.review import Review
from utils.db_helpers import get_session

review_bp = Blueprint("review", __name__)

# ✅ Create a new review
@review_bp.route("/", methods=["POST"])
def create_review():
    data = request.json
    session = get_session()

    try:
        new_review = Review(
            rating=data["rating"],
            product_id=data["product_id"],
            buyer_id=data["buyer_id"]
        )
        session.add(new_review)
        session.commit()
        return jsonify({"message": "Review created successfully", "review_id": new_review.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


# ✅ Get all reviews
@review_bp.route("/", methods=["GET"])
def get_all_reviews():
    session = get_session()
    try:
        reviews = session.query(Review).all()
        result = []
        for review in reviews:
            result.append({
                "id": review.id,
                "rating": review.rating,
                "product_id": review.product_id,
                "buyer_id": review.buyer_id
            })
        return jsonify(result)
    finally:
        session.close()


# ✅ Get review by ID
@review_bp.route("/<int:review_id>", methods=["GET"])
def get_review(review_id):
    session = get_session()
    try:
        review = session.query(Review).get(review_id)
        if not review:
            return jsonify({"error": "Review not found"}), 404

        result = {
            "id": review.id,
            "rating": review.rating,
            "product_id": review.product_id,
            "buyer_id": review.buyer_id
        }
        return jsonify(result)
    finally:
        session.close()
