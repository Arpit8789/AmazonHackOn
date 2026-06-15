# =========================================================
# /api/seller/autolist — Seller Dashboard Batch Route
# Combines grade + price + listing in one call
# =========================================================

import time
from fastapi import APIRouter, UploadFile, File, Form
from typing import List

from models.grading import grade_images
from models.pricing import predict_price
from models.listing import generate_listing

router = APIRouter()


@router.post("/api/seller/autolist")
async def autolist(
    images: List[UploadFile] = File(...),
    product_name: str = Form("Product"),
    category: str = Form("Electronics"),
    original_price: float = Form(2999),
    weight_kg: float = Form(0.5),
):
    """
    Seller dashboard: photos → grade + price + listing in one call.
    Returns combined result with time tracking.
    """
    start_time = time.time()

    # ── Step 1: Grade ─────────────────────────────────
    image_bytes_list = []
    for img in images:
        data = await img.read()
        image_bytes_list.append(data)

    grade_result = grade_images(image_bytes_list)

    # ── Step 2: Price ─────────────────────────────────
    # Estimate warranty and age for seller returns
    warranty_pct = 80 if grade_result["grade"] == "A" else 60 if grade_result["grade"] == "B" else 30
    age_days = 30 if grade_result["grade"] == "A" else 90 if grade_result["grade"] == "B" else 200

    price_result = predict_price(
        warranty_remaining_percent=warranty_pct,
        original_price=original_price,
        product_age_days=age_days,
        demand_score=0.75,  # assume medium-high for seller flow
        weight_kg=weight_kg,
        delivery_zone="city",
        product_category=category,
    )

    # ── Step 3: Listing ───────────────────────────────
    resale_price = price_result.get("price_high", int(original_price * 0.6))

    listing_result = await generate_listing(
        grade=grade_result["grade"],
        product_name=product_name,
        product_category=category,
        defects_description=grade_result.get("defects_description", ""),
        original_price=int(original_price),
        resale_price=resale_price,
        warranty_pct=warranty_pct,
    )

    elapsed = round(time.time() - start_time, 1)

    return {
        "status": "success",
        "data": {
            "grade": grade_result,
            "price": price_result,
            "listing": listing_result,
            "processing_time_seconds": elapsed,
            "time_saved_minutes": 25,
        },
    }
