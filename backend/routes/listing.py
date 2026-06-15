# =========================================================
# /api/generate-listing — Listing Generation Route
# =========================================================

from fastapi import APIRouter
from pydantic import BaseModel

from models.listing import generate_listing

router = APIRouter()


class ListingRequest(BaseModel):
    grade: str = "A"
    product_name: str
    product_category: str = "Electronics"
    defects_description: str = ""
    original_price: int = 2999
    resale_price: int = 2200
    warranty_pct: float = 50


@router.post("/api/generate-listing")
async def create_listing(req: ListingRequest):
    """
    Generate an Amazon-style product listing (title, description, tags).
    Simulates 2-second AI inference delay.
    """
    result = await generate_listing(
        grade=req.grade,
        product_name=req.product_name,
        product_category=req.product_category,
        defects_description=req.defects_description,
        original_price=req.original_price,
        resale_price=req.resale_price,
        warranty_pct=req.warranty_pct,
    )

    return {"status": "success", "data": result}
