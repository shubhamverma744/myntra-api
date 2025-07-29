from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.config import Base

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))

    reviews = relationship("Review", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")
    addresses = relationship("SavedAddress", back_populates="buyer")