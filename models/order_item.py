from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")
