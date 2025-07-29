from flask import Blueprint, request, jsonify
from db.session import get_session
from models.order import Order
from models.cart_item import CartItem
from models.product import Product
from datetime import datetime

order_bp = Blueprint("order", __name__)

# 🔸 Place an Order (from cart)
@order_bp.route('/place', methods=['POST'])
def place_order():
    data = request.get_json()
    buyer_id = data.get("buyer_id")

    if not buyer_id:
        return jsonify({"error": "Missing buyer_id"}), 400

    session = get_session()
    try:
        cart_items = session.query(CartItem).filter_by(buyer_id=buyer_id).all()
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        total_price = 0
        for item in cart_items:
            product = session.query(Product).filter_by(id=item.product_id).first()
            if not product:
                continue  # Skip if product not found
            total_price += product.selling_price * item.quantity

        order = Order(
            buyer_id=buyer_id,
            total_price=total_price,
            order_status="Pending",
            payment_status="Pending",
            order_date=datetime.utcnow()
        )
        session.add(order)
        session.commit()

        # Clear cart items
        for item in cart_items:
            session.delete(item)
        session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_price": order.total_price
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# 🔸 Get All Orders by Buyer (with pagination)
@order_bp.route('/<int:buyer_id>', methods=['GET'])
def get_orders_by_buyer(buyer_id):
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))

    session = get_session()
    try:
        orders = session.query(Order)\
            .filter_by(buyer_id=buyer_id)\
            .order_by(Order.order_date.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()

        result = [{
            "order_id": o.id,
            "total_price": o.total_price,
            "order_status": o.order_status,
            "payment_status": o.payment_status,
            "order_date": o.order_date.isoformat()
        } for o in orders]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# 🔸 Update Order Status (admin/seller)
@order_bp.route('/status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()

    session = get_session()
    try:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        order.order_status = data.get("order_status", order.order_status)
        order.payment_status = data.get("payment_status", order.payment_status)
        session.commit()

        return jsonify({"message": "Order updated successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


