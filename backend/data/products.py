# =========================================================
# Demo Product Catalog — 6 products for all flows
# =========================================================

DEMO_PRODUCTS = [
    {
        "product_id": "P001",
        "name": "Voltas 1.5 Ton 5 Star Inverter Split AC",
        "category": "Appliances",
        "subcategory": "Air Conditioners",
        "original_price": 42990,
        "weight_kg": 45.0,
        "warranty_months": 120,
        "purchase_date": "2026-02-15",
        "order_id": "403-5551234-3334567",
        "image_url": "/product1_ac.jpg",
        "description": "Variable speed compressor, Copper condenser, Anti-dust filter.",
        "resale_eligible": True,
    },
    {
        "product_id": "P002",
        "name": "Nike Air Max 270 Running Shoes",
        "category": "Apparel",
        "subcategory": "Shoes",
        "original_price": 12995,
        "weight_kg": 0.8,
        "warranty_months": 6,
        "purchase_date": "2026-03-22",
        "order_id": "403-9876543-2109876",
        "image_url": "/product2_shoes.jpg",
        "description": "Breathable mesh upper, foam midsole, Max Air unit for cushioning.",
        "resale_eligible": True,
    },
    {
        "product_id": "P003",
        "name": "Sony Noise Cancelling Wireless Headphones",
        "category": "Electronics",
        "subcategory": "Headphones",
        "original_price": 29990,
        "weight_kg": 0.25,
        "warranty_months": 12,
        "purchase_date": "2026-06-01",
        "order_id": "403-7778899-1112233",
        "image_url": "/product3_headphones.jpg",
        "description": "Industry-leading noise cancellation, 30 hours battery life.",
        "resale_eligible": False,
    }
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
