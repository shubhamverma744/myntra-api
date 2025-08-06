from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.sqlite import JSON
from db.config import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50), unique=True, nullable=False)
    product_summary = Column(String(255))
    product_description = Column(Text)
    product_details = Column(JSON)  # Structured key-value details

    product_type = Column(String(50), nullable=False)
    product_category = Column(String(50), nullable=False)
    product_sub_category = Column(String(50))
    brand = Column(String(50), nullable=False)
    gender = Column(String(20))
    age_group = Column(String(20))

    sizes_available = Column(JSON)  # List of sizes (["6", "7", "8", ...])
    colors_available = Column(JSON)  # List of colors

    material = Column(String(50))
    pattern = Column(String(50))
    fit_type = Column(String(50))
    occasion = Column(String(50))
    fabric_care = Column(String(100))

    mrp = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    offers = Column(JSON)

    stock_quantity = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, default=5)

    main_image_url = Column(String(255))
    additional_image_urls = Column(JSON)  # List of image URLs
    video_url = Column(String(255))

    delivery_charge = Column(Float, default=0.0)
    cod_available = Column(Boolean, default=True)
    dispatch_time = Column(Integer, default=2)
    max_delivery_days = Column(Integer, default=5)

    returnable = Column(Boolean, default=True)
    return_days = Column(Integer, default=15)
    exchange_available = Column(Boolean, default=True)
    warranty = Column(String(100))

    meta_title = Column(String(255))
    meta_description = Column(String(255))
    search_tags = Column(JSON)

    hsn_code = Column(String(20))
    gst_percentage = Column(Float)
    country_of_origin = Column(String(50))

    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="products")

    reviews = relationship("Review", back_populates="product", cascade="all, delete")
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")
