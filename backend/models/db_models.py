from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    original_price = Column(Float)
    image_url = Column(String)
    
    # Second Life Specific
    is_second_life = Column(Boolean, default=False)
    second_life_grade = Column(String, nullable=True) # A, B, C
    second_life_price = Column(Float, nullable=True)
    seller_id = Column(String, nullable=True)

    # Relationships
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)  # Mock user ID
    product_db_id = Column(Integer, ForeignKey("products.id"))
    purchase_date = Column(String)
    warranty_months = Column(Integer)
    weight_kg = Column(Float)
    
    # Returns / Resale State
    status = Column(String, default="DELIVERED") # DELIVERED, RETURN_INITIATED, RESALE_LISTED
    return_eligible = Column(Boolean, default=True)
    resell_eligible = Column(Boolean, default=True)
    
    # Relationships
    product = relationship("Product", back_populates="orders")
