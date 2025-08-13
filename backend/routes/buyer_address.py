from flask import Blueprint, request, jsonify, session
from models import BuyerAddress, SellerAddress
from utils.db_helpers import get_session

address_bp = Blueprint("buyer_address", __name__)

# ------------- BUYER ADDRESS ROUTES --------------

@address_bp.route("/buyer-address-save", methods=["POST"])
def save_buyer_address():
    data = request.json
    session_db = get_session()
    buyer_id = session.get("buyer_id")

    if not buyer_id:
        return jsonify({"error": "Unauthorized. Buyer not logged in."}), 401

    try:
        new_address = BuyerAddress(
            buyer_id=buyer_id,
            address_line=data["address_line"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"]
        )
        session_db.add(new_address)
        session_db.commit()
        return jsonify({"message": "Buyer address saved", "address_id": new_address.id}), 201
    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session_db.close()


@address_bp.route("/buyer-address", methods=["GET"])
def get_buyer_addresses():
    session_db = get_session()
    buyer_id = session.get("buyer_id")

    if not buyer_id:
        return jsonify({"error": "Unauthorized. Buyer not logged in."}), 401

    try:
        addresses = session_db.query(BuyerAddress).filter_by(buyer_id=buyer_id).all()
        return jsonify([
            {
                "id": a.id,
                "address_line": a.address_line,
                "city": a.city,
                "state": a.state,
                "zip_code": a.zip_code,
                "country": a.country
            } for a in addresses
        ])
    finally:
        session_db.close()


@address_bp.route("/buyer-address/delete/<int:address_id>", methods=["DELETE"])
def delete_buyer_address(address_id):
    session_db = get_session()
    buyer_id = session.get("buyer_id")

    if not buyer_id:
        return jsonify({"error": "Unauthorized. Buyer not logged in."}), 401

    try:
        address = session_db.query(BuyerAddress).filter_by(id=address_id, buyer_id=buyer_id).first()
        if not address:
            return jsonify({"error": "Address not found or not authorized"}), 404
        session_db.delete(address)
        session_db.commit()
        return jsonify({"message": "Buyer address deleted"})
    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session_db.close()


# ------------- SELLER ADDRESS ROUTES --------------

@address_bp.route("/seller-address/save", methods=["POST"])
def save_seller_address():
    data = request.json
    session_db = get_session()
    seller_id = session.get("seller_id")

    if not seller_id:
        return jsonify({"error": "Unauthorized. Seller not logged in."}), 401

    try:
        new_address = SellerAddress(
            seller_id=seller_id,
            address_line=data["address_line"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"]
        )
        session_db.add(new_address)
        session_db.commit()
        return jsonify({"message": "Seller address saved", "address_id": new_address.id}), 201
    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session_db.close()


@address_bp.route("/seller-address", methods=["GET"])
def get_seller_addresses():
    session_db = get_session()
    seller_id = session.get("seller_id")

    if not seller_id:
        return jsonify({"error": "Unauthorized. Seller not logged in."}), 401

    try:
        addresses = session_db.query(SellerAddress).filter_by(seller_id=seller_id).all()
        return jsonify([
            {
                "id": a.id,
                "address_line": a.address_line,
                "city": a.city,
                "state": a.state,
                "zip_code": a.zip_code,
                "country": a.country
            } for a in addresses
        ])
    finally:
        session_db.close()


@address_bp.route("/seller-address/delete/<int:address_id>", methods=["DELETE"])
def delete_seller_address(address_id):
    session_db = get_session()
    seller_id = session.get("seller_id")

    if not seller_id:
        return jsonify({"error": "Unauthorized. Seller not logged in."}), 401

    try:
        address = session_db.query(SellerAddress).filter_by(id=address_id, seller_id=seller_id).first()
        if not address:
            return jsonify({"error": "Address not found or not authorized"}), 404
        session_db.delete(address)
        session_db.commit()
        return jsonify({"message": "Seller address deleted"})
    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session_db.close()
