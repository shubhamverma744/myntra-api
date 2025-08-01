from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

    # Relationships (optional, useful for eager loading)
    buyer = relationship("Buyer", back_populates="cart_items")
    product = relationship("Product")
