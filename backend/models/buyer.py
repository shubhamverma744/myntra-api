from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.config import Base

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(25), unique=True, nullable=True)
    offical_name = Column(String(200), unique=True, nullable=True)
    signature = Column(String(30), unique=False, nullable=True)


    reviews = relationship("Review", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")
    buyer_addresses = relationship("BuyerAddress", back_populates="buyer", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="buyer", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="buyer", cascade="all, delete-orphan")


    
