from flask import Blueprint, request, jsonify
from models import PaymentDetail
# from db.config import get_session
from utils.db_helpers import get_session
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

# ✅ Create a new payment
@payment_bp.route('/', methods=['POST'])
def create_payment():
    data = request.json
    session = get_session()
    try:
        new_payment = PaymentDetail(
            order_id=data['order_id'],
            payment_mode=data.get('payment_mode'),
            payment_status=data.get('payment_status'),
            paid_at=datetime.utcnow(),
            amount_paid=data.get('amount_paid')
        )
        session.add(new_payment)
        session.commit()
        return jsonify({"message": "Payment created successfully", "payment_id": new_payment.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# ✅ Get all payments
@payment_bp.route('/', methods=['GET'])
def list_payments():
    session = get_session()
    try:
        payments = session.query(PaymentDetail).all()
        result = [{
            "id": p.id,
            "order_id": p.order_id,
            "payment_mode": p.payment_mode,
            "payment_status": p.payment_status,
            "paid_at": p.paid_at,
            "amount_paid": p.amount_paid
        } for p in payments]
        return jsonify(result), 200
    finally:
        session.close()

# ✅ Get one payment by ID
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    session = get_session()
    try:
        payment = session.query(PaymentDetail).get(payment_id)
        if payment:
            result = {
                "id": payment.id,
                "order_id": payment.order_id,
                "payment_mode": payment.payment_mode,
                "payment_status": payment.payment_status,
                "paid_at": payment.paid_at,
                "amount_paid": payment.amount_paid
            }
            return jsonify(result), 200
        return jsonify({"error": "Payment not found"}), 404
    finally:
        session.close()
