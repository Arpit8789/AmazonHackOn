# =========================================================
# /api/resale/list — Submit P2P Listing Route
# =========================================================

import uuid
import random
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Product

router = APIRouter()

# In-memory listing storage
_listings = []


class ResaleListRequest(BaseModel):
    product_id: str
    seller_id: str = "demo_user"
    price_confirmed: float
    delivery_zone: str = "city"
    warranty_remaining_percent: float = 50


@router.post("/api/resale/list")
async def submit_listing(req: ResaleListRequest, db: Session = Depends(get_db)):
    """
    Accept a finalized P2P listing and return a mock listing ID.
    """
    listing_id = f"SL-{uuid.uuid4().hex[:8].upper()}"
    estimated_days = random.randint(3, 10)

    listing = {
        "listing_id": listing_id,
        "product_id": req.product_id,
        "seller_id": req.seller_id,
        "price": req.price_confirmed,
        "delivery_zone": req.delivery_zone,
        "warranty_remaining_percent": req.warranty_remaining_percent,
        "status": "live",
    }

    _listings.append(listing)

    # Persist to database so it shows on the homepage
    product = db.query(Product).filter(Product.product_id == req.product_id).first()
    if product:
        product.is_second_life = True
        product.second_life_price = req.price_confirmed
        product.second_life_grade = "A" # Hidden from user now, default to A
        product.seller_id = req.seller_id
        db.commit()

    return {
        "status": "success",
        "data": {
            "listing_id": listing_id,
            "status": "live",
            "listing_url": f"/second-life/listing/{listing_id}",
            "estimated_sale_days": estimated_days,
            "message": f"Your product is now live on Amazon Second Life! Expected sale within {estimated_days} days.",
        },
    }


def get_all_listings() -> list:
    """Return all stored listings."""
    return _listings
