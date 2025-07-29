from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    file_url = Column(String(255), nullable=False)

    review_id = Column(Integer, ForeignKey('reviews.id'))
    review = relationship("Review", back_populates="attachments")
