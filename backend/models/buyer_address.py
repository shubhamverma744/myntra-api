from sqlalchemy import Column, Integer, String, ForeignKey
from db.config import Base
from sqlalchemy.orm import relationship


class BuyerAddress(Base):
    __tablename__ = 'buyer_addresses'

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)
    address_line = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    country = Column(String(50))
    
    buyer = relationship("Buyer", back_populates="buyer_addresses")
