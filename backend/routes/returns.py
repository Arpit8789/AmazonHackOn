# =========================================================
# /api/return/initiate — Return Flow Trigger Route
# =========================================================

from fastapi import APIRouter
from pydantic import BaseModel

from data.demand_map import get_demand

router = APIRouter()


class ReturnInitiateRequest(BaseModel):
    order_id: str
    product_name: str
    product_category: str
    return_reason: str
    pincode: str = "110001"
    original_price: float = 0


DEFAULT_ANGLES = ["Image 1", "Image 2", "Image 3", "Image 4 (Optional)"]


@router.post("/api/return/initiate")
async def initiate_return(req: ReturnInitiateRequest):
    """
    Accept a return request, check demand, return next steps.
    """
    demand = get_demand(req.pincode)
    angles = DEFAULT_ANGLES

    return {
        "status": "success",
        "data": {
            "order_id": req.order_id,
            "next_step": "photo_upload",
            "photo_count_required": len(angles),
            "angle_guide": angles,
            "instructions": "Try to upload 3 to 4 images from all dimensions for getting correct resale and return evaluation.",
            "demand_info": demand,
        },
    }
