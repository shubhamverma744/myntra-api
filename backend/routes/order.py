from flask import Blueprint, request, jsonify, session as flask_session
from db.config import SessionLocal
from models import Order, OrderItem, Buyer, Product
from datetime import datetime

order_bp = Blueprint("order", __name__)
db_session = SessionLocal


@order_bp.route("/place", methods=["POST"])
def place_order():
    session = db_session()
    data = request.get_json()

    try:
        # ✅ Get buyer ID from session
        buyer_id = flask_session.get("buyer_id")
        if not buyer_id:
            return jsonify({"error": "User not logged in"}), 401

        order_items_data = data.get("order_items", [])
        if not order_items_data:
            return jsonify({"error": "No order items provided"}), 400

        # ✅ Validate buyer exists
        buyer = session.query(Buyer).filter_by(id=buyer_id).first()
        if not buyer:
            return jsonify({"error": "Buyer not found"}), 404

        total_amount = 0.0
        valid_order_items = []

        # ✅ Validate products & calculate total
        for item in order_items_data:
            product = session.query(Product).filter_by(id=item["product_id"]).first()
            if not product:
                return jsonify({"error": f"Product ID {item['product_id']} not found"}), 404

            quantity = int(item.get("quantity", 1))
            if quantity <= 0:
                return jsonify({"error": f"Invalid quantity for product ID {product.id}"}), 400

            # ✅ Snapshot unit price from DB
            unit_price = float(product.mrp)
            total_price = unit_price * quantity
            total_amount += total_price

            valid_order_items.append({
                "product_id": product.id,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "product_name": product.product_name,
                "product_code": product.product_code,
                "selected_size": item.get("selected_size"),
                "selected_color": item.get("selected_color")
            })

        # ✅ Create Order
        order = Order(
            buyer_id=buyer_id,
            total_amount=total_amount,
            created_at=datetime.now()
        )
        session.add(order)
        session.flush()  # get order.id before adding items

        # ✅ Add order items
        for item in valid_order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item["total_price"],
                product_name=item["product_name"],
                product_code=item["product_code"],
                selected_size=item["selected_size"],
                selected_color=item["selected_color"]
            )
            session.add(order_item)

        session.commit()
        session.refresh(order)

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id,
            "buyer_id": order.buyer_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at.isoformat(),
            "order_items": valid_order_items
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


# Get All Orders
@order_bp.route("/list", methods=["GET"])
def get_orders_list():
    session = db_session()
    try:
        orders = session.query(Order).all()
        return jsonify([
            {
                "id": o.id,
                "buyer_id": o.buyer_id,
                "total_amount": o.total_amount,
                "created_at": o.created_at.isoformat()
            }
            for o in orders
        ]), 200
    finally:
        session.close()


# Get Order by ID
@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    session = db_session()
    try:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({
            "id": order.id,
            "buyer_id": order.buyer_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at.isoformat()
        }), 200
    finally:
        session.close()


# Delete Order
@order_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    session = db_session()
    try:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        session.delete(order)
        session.commit()
        return jsonify({"message": "Order deleted"}), 200
    finally:
        session.close()
