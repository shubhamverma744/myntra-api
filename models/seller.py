from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from db.config import Base

class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, primary_key=True, nullable=False)
    password = Column(String(100), nullable=False)
    official_name = Column(String(100), nullable=False)
    kyc = Column(String(100))
    seller_rating = Column(Float, default=0.0)
    since_active = Column(Date, nullable=False)
    address = Column(String(200), nullable=False)

    products = relationship("Product", back_populates="seller", cascade="all, delete")
