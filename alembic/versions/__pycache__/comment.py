from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(300), nullable=False)

    review_id = Column(Integer, ForeignKey('reviews.id'))
    review = relationship("Review", back_populates="comments")
