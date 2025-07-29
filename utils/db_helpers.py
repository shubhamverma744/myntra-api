from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from db.config import engine
from models import Buyer, Seller, Product, Order, OrderItem, SavedAddress

# ========== DB SESSION HELPERS ==========

SessionLocal = scoped_session(sessionmaker(bind=engine))

def get_session():
    """Get a new scoped session."""
    return SessionLocal()

def commit_with_rollback(session):
    """Commit the session or rollback on failure."""
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e


# ========== BUYER HELPERS ==========

def create_buyer(data):
    session = get_session()
    try:
        buyer = Buyer(**data)
        session.add(buyer)
        commit_with_rollback(session)
        session.refresh(buyer)
        return buyer
    finally:
        session.close()

def get_buyer_by_id(buyer_id):
    session = get_session()
    try:
        return session.get(Buyer, buyer_id)
    finally:
        session.close()


# ========== SELLER HELPERS ==========

def get_seller_by_id(seller_id):
    session = get_session()
    try:
        return session.get(Seller, seller_id)
    finally:
        session.close()


# ========== PRODUCT HELPERS ==========

def get_all_products():
    session = get_session()
    try:
        return session.query(Product).all()
    finally:
        session.close()

def get_product_by_id(product_id):
    session = get_session()
    try:
        return session.get(Product, product_id)
    finally:
        session.close()

def get_products_by_seller(seller_id):
    session = get_session()
    try:
        return session.query(Product).filter_by(seller_id=seller_id).all()
    finally:
        session.close()


# ========== ORDER HELPERS ==========

def create_order(buyer_id, items):
    session = get_session()
    try:
        order = Order(buyer_id=buyer_id, total_amount=0)
        session.add(order)
        session.flush()

        total = 0
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            price = 100  # TODO: fetch from Product table

            order_item = OrderItem(
                order_id=order.id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(order_item)
            total += price * quantity

        order.total_amount = total
        commit_with_rollback(session)
        session.refresh(order)
        return order
    finally:
        session.close()

def get_order_by_id(order_id):
    session = get_session()
    try:
        return session.get(Order, order_id)
    finally:
        session.close()


# ========== ADDRESS HELPERS ==========

def add_address(buyer_id, address_data):
    session = get_session()
    try:
        address = SavedAddress(buyer_id=buyer_id, **address_data)
        session.add(address)
        commit_with_rollback(session)
        session.refresh(address)
        return address
    finally:
        session.close()

def get_addresses_for_buyer(buyer_id):
    session = get_session()
    try:
        return session.query(SavedAddress).filter_by(buyer_id=buyer_id).all()
    finally:
        session.close()


# Add product 
def add_product(product_data):
    """
    Adds a new product to the database.

    :param product_data: dict containing product fields
    :return: the created Product object
    """
    session = get_session()
    try:
        new_product = Product(**product_data)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()