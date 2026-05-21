from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    category = Column(String, index=True) # e.g., "Burgers", "Pharmacy", "Groceries"
    is_active = Column(Boolean, default=True)
    city = Column(String, index=True)