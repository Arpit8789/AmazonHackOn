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
        name="JBL Flip 6 Portable Bluetooth Speaker (Pre-Owned)",
        category="Electronics",
        original_price=11999,
        image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&q=80",
        is_second_life=True,
        second_life_grade="B",
        second_life_price=6999,
        seller_id="user_123"
    )
    db.add(second_life_product)
    
    db.commit()
    
    print("Seeding Orders...")
    
    # Create orders for the products so they show up in "Your Orders"
    # We assign different statuses to mimic the UI requirement
    # "in two products give the option of resell and in two products give the option of return"
    
    # Product 1: Eligible for Resell (Smartwatch)
    order1 = Order(
        order_id="ORD-1001",
        user_id="user_123",
        product_db_id=1,  # P001 Smartwatch
        purchase_date="12 Jan 2026",
        warranty_months=12,
        weight_kg=0.12,
        status="DELIVERED",
        return_eligible=False, # Too old for return
        resell_eligible=True
    )
    db.add(order1)
    
    # Product 2: Eligible for Resell (Baby Monitor)
    order2 = Order(
        order_id="ORD-1002",
        user_id="user_123",
        product_db_id=3,  # P003 Baby Monitor
        purchase_date="15 Feb 2026",
        warranty_months=18,
        weight_kg=0.8,
        status="DELIVERED",
        return_eligible=False,
        resell_eligible=True
    )
    db.add(order2)
    
    # Product 3: Eligible for Return (Water Bottle) - CHEAP
    order3 = Order(
        order_id="ORD-1003",
        user_id="user_123",
        product_db_id=4,  # P004 Water Bottle
        purchase_date="10 Jun 2026", # Recent
        warranty_months=12,
        weight_kg=0.4,
        status="DELIVERED",
        return_eligible=True,
        resell_eligible=False
    )
    db.add(order3)
    
    # Product 4: Eligible for Return (Yoga Mat) - CHEAP
    order4 = Order(
        order_id="ORD-1004",
        user_id="user_123",
        product_db_id=5,  # P005 Yoga Mat
        purchase_date="12 Jun 2026", # Recent
        warranty_months=3,
        weight_kg=1.2,
        status="DELIVERED",
        return_eligible=True,
        resell_eligible=False
    )
    db.add(order4)

    # Product 5: Window Closed (Mouse)
    order5 = Order(
        order_id="ORD-1005",
        user_id="user_123",
        product_db_id=6,  # P006 Mouse
        purchase_date="10 Jan 2023", # Too old for both
        warranty_months=36,
        weight_kg=0.1,
        status="DELIVERED",
        return_eligible=False,
        resell_eligible=False
    )
    db.add(order5)

    db.commit()
    db.close()
    
    print("Seeding complete! Data is now live in NeonDB.")

if __name__ == "__main__":
    seed()
