from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="reviews")

    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    buyer = relationship("Buyer", back_populates="reviews")

    comments = relationship("Comment", back_populates="review", cascade="all, delete")
    attachments = relationship("Attachment", back_populates="review", cascade="all, delete")
