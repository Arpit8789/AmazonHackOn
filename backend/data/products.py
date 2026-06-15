# =========================================================
# Demo Product Catalog — 6 products for all flows
# =========================================================

DEMO_PRODUCTS = [
    {
        "product_id": "P001",
        "name": "JBL Flip 6 Portable Bluetooth Speaker",
        "category": "Electronics",
        "subcategory": "Speakers",
        "original_price": 11999,
        "weight_kg": 0.55,
        "warranty_months": 12,
        "purchase_date": "2026-01-10",
        "order_id": "403-1234567-8901234",
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&q=80",
        "description": "Eco-friendly design, IP67 waterproof, 12 hours playtime, PartyBoost.",
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
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80",
        "description": "Breathable mesh upper, foam midsole, Max Air unit for cushioning.",
        "resale_eligible": True,
    },
    {
        "product_id": "P003",
        "name": "Voltas 1.5 Ton 5 Star Inverter Split AC",
        "category": "Appliances",
        "subcategory": "Air Conditioners",
        "original_price": 42990,
        "weight_kg": 45.0,
        "warranty_months": 120,
        "purchase_date": "2026-02-15",
        "order_id": "403-5551234-3334567",
        "image_url": "https://images.unsplash.com/photo-1616137422495-1e9e46e2aa77?w=400&q=80",
        "description": "Variable speed compressor, Copper condenser, Anti-dust filter.",
        "resale_eligible": True,
    },
    {
        "product_id": "P004",
        "name": "Puma Smash v2 L Sneakers",
        "category": "Apparel",
        "subcategory": "Shoes",
        "original_price": 2999,
        "weight_kg": 0.6,
        "warranty_months": 3,
        "purchase_date": "2026-06-01",
        "order_id": "403-7778899-1112233",
        "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614c3a?w=400&q=80",
        "description": "Soft leather upper, durable rubber outsole, classic tennis-inspired look.",
        "resale_eligible": False,
    },
    {
        "product_id": "P005",
        "name": "Sony SRS-XB13 Extra Bass Speaker",
        "category": "Electronics",
        "subcategory": "Speakers",
        "original_price": 3990,
        "weight_kg": 0.25,
        "warranty_months": 12,
        "purchase_date": "2026-06-05",
        "order_id": "403-4445566-7788990",
        "image_url": "https://images.unsplash.com/photo-1589003071617-10ce6bcf6418?w=400&q=80",
        "description": "Compact size, multiway strap, up to 16 hours battery, IP67 rating.",
        "resale_eligible": False,
    },
    {
        "product_id": "P006",
        "name": "Adidas Ultraboost 22 Running Shoes",
        "category": "Apparel",
        "subcategory": "Shoes",
        "original_price": 17999,
        "weight_kg": 0.7,
        "warranty_months": 6,
        "purchase_date": "2023-01-10",
        "order_id": "403-1112233-4455667",
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80",
        "description": "BOOST midsole, Continental Rubber outsole, made with recycled materials.",
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
