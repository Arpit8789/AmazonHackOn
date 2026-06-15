# =========================================================
# /api/price — XGBoost Pricing Route
# =========================================================

from fastapi import APIRouter
from pydantic import BaseModel

from models.pricing import predict_price

router = APIRouter()


class PriceRequest(BaseModel):
    warranty_remaining_percent: float
    original_price: float
    product_category: str = "Electronics"
    product_age_days: int = 180
    weight_kg: float = 0.5
    delivery_zone: str = "city"  # local / city / regional / national
    demand_score: float = 0.7


@router.post("/api/price")
async def calculate_price(req: PriceRequest):
    """
    Calculate resale price with SHAP explanation and full charge breakdown.
    """
    result = predict_price(
        warranty_remaining_percent=req.warranty_remaining_percent,
        original_price=req.original_price,
        product_age_days=req.product_age_days,
        demand_score=req.demand_score,
        weight_kg=req.weight_kg,
        delivery_zone=req.delivery_zone,
        product_category=req.product_category,
    )

    return {"status": "success", "data": result}
