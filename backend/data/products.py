# =========================================================
# Demo Product Catalog — 6 products for all flows
# =========================================================

DEMO_PRODUCTS = [
    {
        "product_id": "P001",
        "name": "Noise ColorFit Pro 4 Smartwatch",
        "category": "Electronics",
        "subcategory": "Smartwatches",
        "original_price": 3499,
        "weight_kg": 0.12,
        "warranty_months": 12,
        "purchase_date": "2026-01-10",
        "order_id": "403-1234567-8901234",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80",
        "description": "1.72\" AMOLED display, Bluetooth calling, 100+ sports modes, SpO2, heart rate monitor.",
        "resale_eligible": True,
    },
    {
        "product_id": "P002",
        "name": "boAt Rockerz 450 Bluetooth Headphones",
        "category": "Electronics",
        "subcategory": "Headphones",
        "original_price": 2999,
        "weight_kg": 0.25,
        "warranty_months": 12,
        "purchase_date": "2026-03-22",
        "order_id": "403-9876543-2109876",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80",
        "description": "40mm drivers, 15-hour battery, padded ear cushions, Bluetooth 5.0, foldable design.",
        "resale_eligible": True,
    },
    {
        "product_id": "P003",
        "name": "Philips Avent Baby Monitor SCD841",
        "category": "Baby Products",
        "subcategory": "Baby Monitors",
        "original_price": 4999,
        "weight_kg": 0.8,
        "warranty_months": 18,
        "purchase_date": "2026-02-15",
        "order_id": "403-5551234-3334567",
        "image_url": "/baby_monitor.jpg",
        "description": "DECT technology, 330m range, temperature sensor, night-light, 18-hour battery.",
        "resale_eligible": True,
    },
    {
        "product_id": "P004",
        "name": "Milton Thermosteel Water Bottle 1L",
        "category": "Home & Kitchen",
        "subcategory": "Water Bottles",
        "original_price": 599,
        "weight_kg": 0.4,
        "warranty_months": 12,
        "purchase_date": "2026-06-01",
        "order_id": "403-7778899-1112233",
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&q=80",
        "description": "1000ml stainless steel vacuum insulated flask, 24 hours hot/cold.",
        "resale_eligible": False,
    },
    {
        "product_id": "P005",
        "name": "Amazon Basics Yoga Mat 6mm",
        "category": "Fitness",
        "subcategory": "Yoga Mats",
        "original_price": 649,
        "weight_kg": 1.2,
        "warranty_months": 3,
        "purchase_date": "2026-06-05",
        "order_id": "403-4445566-7788990",
        "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&q=80",
        "description": "6mm thick, non-slip texture, moisture resistant, includes carrying strap.",
        "resale_eligible": False,
    },
    {
        "product_id": "P006",
        "name": "Logitech M235 Wireless Mouse",
        "category": "Electronics",
        "subcategory": "Accessories",
        "original_price": 799,
        "weight_kg": 0.1,
        "warranty_months": 36,
        "purchase_date": "2023-01-10",
        "order_id": "403-1112233-4455667",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&q=80",
        "description": "Advanced optical tracking, unifying receiver, 12-month battery life.",
        "resale_eligible": False,
    },
]


def get_product(product_id: str) -> dict | None:
    """Get a single product by ID."""
    for p in DEMO_PRODUCTS:
        if p["product_id"] == product_id:
            return p
    return None


def get_all_products() -> list[dict]:
    """Return all demo products."""
    return DEMO_PRODUCTS
