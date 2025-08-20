# models_all.py — Unified models with Base Model, UUID hex IDs & cascading deletes
import uuid
from datetime import datetime, date

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Date,
    ForeignKey,
    Text,
    Boolean,
    UniqueConstraint,
    JSON as SAJSON,
    DECIMAL,
)
from sqlalchemy.orm import relationship, validates

from db.config import Base as SQLAlchemyBase


# Helper to generate 32‑char lowercase hex IDs
def generate_uuid() -> str:
    return uuid.uuid4().hex


# ----------------------------- Base Model -----------------------------
class BaseModel(SQLAlchemyBase):
    __abstract__ = True
    
    id = Column(String(32), primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# ----------------------------- Buyer -----------------------------
class Buyer(BaseModel):
    __tablename__ = "buyers"

    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(25), unique=True, nullable=True)
    # Keeping original field name to avoid breaking migrations
    offical_name = Column(String(200), unique=True, nullable=True)
    signature = Column(String(30), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships (ORM + DB cascades)
    reviews = relationship(
        "Review", back_populates="buyer", cascade="all, delete-orphan", passive_deletes=True
    )
    orders = relationship(
        "Order", back_populates="buyer", cascade="all, delete-orphan", passive_deletes=True
    )
    buyer_addresses = relationship(
        "BuyerAddress", back_populates="buyer", cascade="all, delete-orphan", passive_deletes=True
    )
    cart_items = relationship(
        "CartItem", back_populates="buyer", cascade="all, delete-orphan", passive_deletes=True
    )
    comments = relationship(
        "Comment", back_populates="buyer", cascade="all, delete-orphan", passive_deletes=True
    )

    @validates('email')
    def validate_email(self, key, email):
        import re
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email format")
        return email.lower()


# -------------------------- BuyerAddress -------------------------
class BuyerAddress(BaseModel):
    __tablename__ = "buyer_addresses"

    buyer_id = Column(String(32), ForeignKey("buyers.id", ondelete="CASCADE"), nullable=False)
    address_line = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(50), nullable=False, default="India")
    is_default = Column(Boolean, default=False)

    buyer = relationship("Buyer", back_populates="buyer_addresses")


# ------------------------------ Seller ---------------------------
class Seller(BaseModel):
    __tablename__ = "sellers"

    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    official_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(25), unique=True, nullable=True)
    kyc = Column(String(100))
    seller_rating = Column(Float, default=0.0)
    since_active = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    products = relationship(
        "Product", back_populates="seller", cascade="all, delete-orphan", passive_deletes=True
    )
    seller_addresses = relationship(
        "SellerAddress", back_populates="seller", cascade="all, delete-orphan", passive_deletes=True
    )

    @validates('seller_rating')
    def validate_rating(self, key, rating):
        if rating is not None and not 0 <= rating <= 5:
            raise ValueError("Seller rating must be between 0 and 5")
        return rating


# -------------------------- SellerAddress ------------------------
class SellerAddress(BaseModel):
    __tablename__ = "seller_addresses"

    seller_id = Column(String(32), ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False)
    address_line = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(50), nullable=False, default="India")
    is_default = Column(Boolean, default=False)

    seller = relationship("Seller", back_populates="seller_addresses")


# ------------------------------ Product --------------------------
class Product(BaseModel):
    __tablename__ = "products"

    seller_id = Column(String(32), ForeignKey("sellers.id", ondelete="CASCADE"))

    # Core info
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    product_summary = Column(String(255))
    product_description = Column(Text)
    product_details = Column(SAJSON)  # structured key-value details

    # Taxonomy
    product_type = Column(String(50), nullable=False)
    product_category = Column(String(50), nullable=False, index=True)
    product_sub_category = Column(String(50))
    brand = Column(String(50), nullable=False, index=True)
    gender = Column(String(20))
    age_group = Column(String(20))

    # Options
    sizes_available = Column(SAJSON)
    colors_available = Column(SAJSON)

    # Attributes
    material = Column(String(50))
    pattern = Column(String(50))
    fit_type = Column(String(50))
    occasion = Column(String(50))
    fabric_care = Column(String(100))

    # Pricing
    mrp = Column(DECIMAL(10, 2), nullable=False)
    selling_price = Column(DECIMAL(10, 2), nullable=False)
    discount = Column(Float, default=0.0)
    offers = Column(SAJSON)

    # Inventory
    stock_quantity = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, default=5)

    # Media
    main_image_url = Column(String(255))
    additional_image_urls = Column(SAJSON)
    video_url = Column(String(255))

    # Shipping
    delivery_charge = Column(DECIMAL(10, 2), default=0.0)
    cod_available = Column(Boolean, default=True)
    dispatch_time = Column(Integer, default=2)
    max_delivery_days = Column(Integer, default=5)

    # Policy
    returnable = Column(Boolean, default=True)
    return_days = Column(Integer, default=15)
    exchange_available = Column(Boolean, default=True)
    warranty = Column(String(100))

    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(255))
    search_tags = Column(SAJSON)

    # Compliance
    hsn_code = Column(String(20))
    gst_percentage = Column(Float)
    country_of_origin = Column(String(50), default="India")

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False)

    # Relationships
    seller = relationship("Seller", back_populates="products")
    reviews = relationship(
        "Review", back_populates="product", cascade="all, delete-orphan", passive_deletes=True
    )
    comments = relationship(
        "Comment", back_populates="product", cascade="all, delete-orphan", passive_deletes=True
    )
    order_items = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan", passive_deletes=True
    )
    cart_items = relationship(
        "CartItem", back_populates="product", cascade="all, delete-orphan", passive_deletes=True
    )

    @validates('stock_quantity')
    def validate_stock(self, key, quantity):
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        return quantity

    @validates('selling_price', 'mrp')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError(f"{key} must be greater than 0")
        return price


# ------------------------------ Review --------------------------
class Review(BaseModel):
    __tablename__ = "reviews"

    rating = Column(Float, nullable=False)
    title = Column(String(200))
    content = Column(Text)

    product_id = Column(String(32), ForeignKey("products.id", ondelete="CASCADE"))
    buyer_id = Column(String(32), ForeignKey("buyers.id", ondelete="CASCADE"))

    # Review status
    is_verified = Column(Boolean, default=False)
    is_helpful_count = Column(Integer, default=0)

    product = relationship("Product", back_populates="reviews")
    buyer = relationship("Buyer", back_populates="reviews")

    attachments = relationship(
        "Attachment", back_populates="review", cascade="all, delete-orphan", passive_deletes=True
    )
    comments = relationship(
        "Comment", back_populates="review", cascade="all, delete-orphan", passive_deletes=True
    )

    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating


# ----------------------------- Attachment ------------------------
class Attachment(BaseModel):
    __tablename__ = "attachments"

    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20))  # image, video
    file_size = Column(Integer)  # in bytes

    review_id = Column(String(32), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    review = relationship("Review", back_populates="attachments")


# ------------------------------ Comment -------------------------
class Comment(BaseModel):
    __tablename__ = "comments"

    buyer_id = Column(String(32), ForeignKey("buyers.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(32), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)

    # Optional link to a review
    review_id = Column(String(32), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    buyer = relationship("Buyer", back_populates="comments")
    product = relationship("Product", back_populates="comments")
    review = relationship("Review", back_populates="comments")

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating


# ------------------------------ Order ---------------------------
class Order(BaseModel):
    __tablename__ = "orders"

    buyer_id = Column(String(32), ForeignKey("buyers.id", ondelete="CASCADE"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Order status tracking
    status = Column(String(20), default="pending", nullable=False)  # pending, confirmed, shipped, delivered, cancelled, returned
    
    # Shipping information
    shipping_address = Column(SAJSON)  # Store full address as JSON
    billing_address = Column(SAJSON)   # Store full address as JSON
    
    # Delivery tracking
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    tracking_number = Column(String(100), nullable=True)
    
    # Order notes
    notes = Column(Text)

    # Relationships
    buyer = relationship("Buyer", back_populates="orders")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan", passive_deletes=True
    )
    payment = relationship(
        "PaymentDetail", back_populates="order", uselist=False, cascade="all, delete-orphan", passive_deletes=True
    )

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return status


# ------------------------------ OrderItem -----------------------
class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(String(32), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(32), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    
    # Product details at time of order (for historical accuracy)
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50), nullable=False)
    
    # Selected options
    selected_size = Column(String(20))
    selected_color = Column(String(30))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        return quantity


# ------------------------------ PaymentDetail -------------------
class PaymentDetail(BaseModel):
    __tablename__ = "payment"  # kept as-is to match your existing table name

    order_id = Column(
        String(32), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    payment_mode = Column(String(50), nullable=False)  # UPI, Card, COD, NetBanking, Wallet
    payment_status = Column(String(20), default="PENDING", nullable=False)  # SUCCESS, FAILED, PENDING, REFUNDED
    amount_paid = Column(DECIMAL(10, 2), nullable=False)
    
    # Transaction details
    transaction_id = Column(String(100), unique=True)
    gateway_response = Column(SAJSON)  # Store gateway response as JSON
    
    # Timestamps
    paid_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="payment")

    __table_args__ = (
        UniqueConstraint("order_id", name="uq_payment_order_id"),  # enforce 1:1 at DB level
    )

    @validates('payment_status')
    def validate_payment_status(self, key, status):
        valid_statuses = ["SUCCESS", "FAILED", "PENDING", "REFUNDED"]
        if status not in valid_statuses:
            raise ValueError(f"Payment status must be one of: {', '.join(valid_statuses)}")
        return status


# ------------------------------ CartItem ------------------------
class CartItem(BaseModel):
    __tablename__ = "cart_items"

    buyer_id = Column(String(32), ForeignKey("buyers.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(32), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    
    # Selected options
    selected_size = Column(String(20))
    selected_color = Column(String(30))
    
    # Price at time of adding to cart
    unit_price = Column(DECIMAL(10, 2))

    buyer = relationship("Buyer", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    # Unique constraint to prevent duplicate cart items for same product with same options
    __table_args__ = (
        UniqueConstraint("buyer_id", "product_id", "selected_size", "selected_color", 
                        name="uq_cart_item_buyer_product_options"),
    )

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Cart item quantity must be greater than 0")
        return quantity
    
# ---------------------------- Category ----------------------------
class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(50), nullable=False, unique=True)

    # One-to-many relationship
    subcategories = relationship(
        "SubCategory",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


# ---------------------------- SubCategory -------------------------
class SubCategory(BaseModel):
    __tablename__ = "subcategories"

    name = Column(String(50), nullable=False)

    category_id = Column(
        String(32),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )

    category = relationship("Category", back_populates="subcategories")

