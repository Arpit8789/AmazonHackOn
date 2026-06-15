import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, SessionLocal
from models.db_models import Product, Order
from data.products import get_all_products # Reusing the old mock data to seed

def seed():
    print("Creating tables in NeonDB...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print("Seeding Products...")
    mock_products = get_all_products()
    
    # Insert Products
    for p_data in mock_products:
        product = Product(
            product_id=p_data["product_id"],
            name=p_data["name"],
            category=p_data["category"],
            original_price=p_data["original_price"],
            image_url=p_data["image_url"],
            is_second_life=False
        )
        db.add(product)
    
    # We add a dummy "Second Life" product to show on the homepage
    second_life_product = Product(
        product_id="P_SL_100",
        name="Voltas 1.5 Ton AC (Pre-Owned)",
        category="Appliances",
        original_price=42990,
        image_url="/product1_ac.jpg",
        is_second_life=True,
        second_life_grade="B",
        second_life_price=28999,
        seller_id="user_123"
    )
    db.add(second_life_product)
    
    db.commit()
    
    print("Seeding Orders...")
    
    # Create orders for the products so they show up in "Your Orders"
    # We assign different statuses to mimic the UI requirement
    # "in two products give the option of resell and in two products give the option of return"
    
    # Product 1: Eligible for Resell (AC)
    order1 = Order(
        order_id="ORD-1001",
        user_id="user_123",
        product_db_id=1,  # P001 AC
        purchase_date="12 Jan 2026",
        warranty_months=120,
        weight_kg=45.0,
        status="DELIVERED",
        return_eligible=False, # Too old for return
        resell_eligible=True
    )
    db.add(order1)
    
    # Product 2: Eligible for Return (Shoes) - CHEAP
    order2 = Order(
        order_id="ORD-1002",
        user_id="user_123",
        product_db_id=2,  # P002 Shoes
        purchase_date="15 Jun 2026", # Recent
        warranty_months=6,
        weight_kg=0.8,
        status="DELIVERED",
        return_eligible=True,
        resell_eligible=False
    )
    db.add(order2)
    
    # Product 3: Window Closed (Headphones)
    order3 = Order(
        order_id="ORD-1003",
        user_id="user_123",
        product_db_id=3,  # P003 Headphones
        purchase_date="10 Jan 2023", # Too old for both
        warranty_months=12,
        weight_kg=0.25,
        status="DELIVERED",
        return_eligible=False,
        resell_eligible=False
    )
    db.add(order3)

    db.commit()
    db.close()
    
    print("Seeding complete! Data is now live in NeonDB.")

if __name__ == "__main__":
    seed()
