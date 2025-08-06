from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.config import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)  # Optional: 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    review_id = Column(Integer, ForeignKey("reviews.id"))  # ✅ Add this
    review = relationship("Review", back_populates="comments")  # ✅ Keep this


    # Relationships
    buyer = relationship("Buyer", back_populates="comments")
    product = relationship("Product", back_populates="comments")
