# =========================================================
# /api/grade — AI Vision Grading Route
# Now uses Gemini Vision (with CLIP fallback)
# Auto-relists Grade A/B items as Second Life products
# =========================================================

import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import List
from sqlalchemy.orm import Session

from models.ai_grading import grade_with_gemini
from models.grading import grade_images, get_routing_decision
from data.demand_map import get_demand
from database import get_db
from models.db_models import Product

logger = logging.getLogger("grade-route")
router = APIRouter()


@router.post("/api/grade")
async def grade_product(
    images: List[UploadFile] = File(...),
    return_reason: str = Form(""),
    product_category: str = Form("Electronics"),
    original_price: float = Form(0),
    pincode: str = Form("110001"),
    product_name: str = Form(""),
    image_url: str = Form("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80"),
    db: Session = Depends(get_db),
):
    """
    Accept product images, grade with Gemini Vision (CLIP fallback),
    and auto-relist Grade A/B items on Second Life.
    """
    # Read all image bytes
    image_bytes_list = []
    for img in images:
        data = await img.read()
        image_bytes_list.append(data)

    # Grade with Gemini Vision (falls back to CLIP automatically)
    grade_result = grade_with_gemini(image_bytes_list, return_reason)

    # Look up regional demand
    demand_info = get_demand(pincode)

    # Determine routing
    routing = get_routing_decision(
        grade=grade_result.get("grade", "C"),
        demand=demand_info["demand"],
        demand_region=demand_info["city"],
    )

    # ── AUTO-RELIST LOGIC ────────────────────────────────────
    # Grade A → Relist at same price
    # Grade B → Relist at 10% discount
    # Grade C/D/Reject → No relist (warehouse)
    grade = grade_result.get("grade", "C")
    relist_info = {"relisted": False}

    if grade in ("A", "B") and original_price > 0:
        if grade == "A":
            final_price = original_price
        else:  # Grade B
            final_price = round(original_price * 0.90)

        # Create a new Second Life product in DB
        try:
            sl_product = Product(
                product_id=f"RET_{db.query(Product).count() + 1}",
                name=product_name if product_name else f"Returned {product_category} Item",
                category=product_category,
                original_price=final_price,
                image_url=image_url,
                is_second_life=False,
                second_life_grade=None,
                second_life_price=None,
                seller_id="user_123"
            )
            db.add(sl_product)
            db.commit()
            relist_info = {
                "relisted": True,
                "final_price": final_price,
                "grade": grade,
            }
            logger.info(f"Auto-relisted returned item as regular item (Grade {grade}) at ₹{final_price}")
        except Exception as e:
            logger.error(f"Failed to auto-relist: {e}")
            db.rollback()

    return {
        "status": "success",
        "data": {
            **grade_result,
            "return_reason": return_reason,
            "product_category": product_category,
            "original_price": original_price,
            "demand_score": demand_info["score"],
            "demand_level": demand_info["demand"],
            "demand_region": demand_info["city"],
            **routing,
            "relist_info": relist_info,
        },
    }
