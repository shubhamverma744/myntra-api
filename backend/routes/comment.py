from flask import Blueprint, request, jsonify
from models import Comment
from utils.db_helpers import get_session
from datetime import datetime

comment_bp = Blueprint("comment", __name__)

# ✅ Create a new comment
@comment_bp.route("/", methods=["POST"])
def create_comment():
    data = request.json
    session = get_session()

    try:
        new_comment = Comment(
            buyer_id=data["buyer_id"],
            product_id=data["product_id"],
            content=data["content"],
            rating=data.get("rating"),
            created_at=datetime.utcnow()
        )
        session.add(new_comment)
        session.commit()
        return jsonify({"message": "Comment created successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

# ✅ Get all comments
@comment_bp.route("/", methods=["GET"])
def get_all_comments():
    session = get_session()
    try:
        comments = session.query(Comment).all()
        result = []
        for comment in comments:
            result.append({
                "id": comment.id,
                "buyer_id": comment.buyer_id,
                "product_id": comment.product_id,
                "content": comment.content,
                "rating": comment.rating,
                "created_at": comment.created_at.isoformat()
            })
        return jsonify(result)
    finally:
        session.close()
