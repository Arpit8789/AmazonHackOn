# =========================================================
# Demo Product Catalog — 6 products for all flows
# =========================================================

DEMO_PRODUCTS = [
    {
        "product_id": "P001",
        "name": "Voltas Convertible Anti-dust 1.5 Ton Inverter Split AC",
        "category": "Appliances",
        "subcategory": "Air Conditioners",
        "original_price": 42990,
        "weight_kg": 45.0,
        "warranty_months": 120,
        "purchase_date": "2026-02-15",
        "order_id": "403-5551234-3334567",
        "image_url": "/product1_ac.jpg",
        "description": "Convertible 4-in-1 cooling mode, copper condenser, anti-dust filter, R32 refrigerant.",
        "resale_eligible": True,
    },
    {
        "product_id": "P002",
        "name": "SPARX Casual Shoe SM-734 White",
        "category": "Apparel",
        "subcategory": "Shoes",
        "original_price": 899,
        "weight_kg": 0.8,
        "warranty_months": 6,
        "purchase_date": "2026-03-22",
        "order_id": "403-9876543-2109876",
        "image_url": "/product2_shoes.jpg",
        "description": "Casual sneakers for men, comfortable fit, durable PVC sole, lace-up design.",
        "resale_eligible": True,
    },
    {
        "product_id": "P003",
        "name": "boAt Stone 352 Pro Bluetooth Speaker",
        "category": "Electronics",
        "subcategory": "Speakers",
        "original_price": 1999,
        "weight_kg": 0.5,
        "warranty_months": 12,
        "purchase_date": "2026-06-01",
        "order_id": "403-7778899-1112233",
        "image_url": "/product3_headphones.jpg",
        "description": "14W RMS stereo sound, up to 12 hours playtime, IPX5 water resistance.",
        "resale_eligible": True,
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
