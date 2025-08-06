from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from db.config import Base
from datetime import datetime

class PaymentDetail(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    payment_mode = Column(String(50))       # e.g., UPI, Card, COD
    payment_status = Column(String(20))     # e.g., SUCCESS, FAILED, PENDING
    paid_at = Column(DateTime, default=datetime.utcnow)
    amount_paid = Column(Float)

    order = relationship("Order", back_populates="payment")
