from sqlalchemy import Column, Integer, String, ForeignKey
from db.config import Base
from sqlalchemy.orm import relationship


class SellerAddress(Base):
    __tablename__ = 'seller_addresses'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    address_line = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    country = Column(String(50))
    
    seller = relationship("Seller", back_populates="seller_addresses")
