# =========================================================
# /api/resale/ai-price — AI-Powered Resale Price Prediction
# Uses Gemini Vision + CatBoost for intelligent pricing
# =========================================================

import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional

from models.ai_grading import grade_with_gemini, calculate_condition_score, assign_grade
from models.ai_pricing import predict_resale_price, calculate_warranty_info

logger = logging.getLogger("ai-resale")
router = APIRouter()


@router.post("/api/resale/ai-price")
async def ai_resale_price(
    images: List[UploadFile] = File(...),
    description: str = Form(""),
    product_category: str = Form("Electronics"),
    brand: str = Form("Unknown"),
    product_name: str = Form("Unknown Product"),
    purchase_price: float = Form(...),
    current_market_price: Optional[float] = Form(None),
    purchase_date: str = Form(...),
    initial_warranty_days: int = Form(365),
):
    """
    Full AI resale pricing pipeline:
    1. Gemini Vision inspects product images → condition score + grade
    2. CatBoost predicts fair resale price with SHAP explanation
    3. Returns comprehensive pricing + grading report
    """
    if not images:
        raise HTTPException(status_code=400, detail="At least one image is required.")

    if purchase_price <= 0:
        raise HTTPException(status_code=400, detail="purchase_price must be positive.")

    # Use purchase_price as market price if not provided
    if current_market_price is None or current_market_price <= 0:
        current_market_price = purchase_price

    # 1. Read image bytes
    image_bytes_list = []
    for img in images[:3]:
        data = await img.read()
        image_bytes_list.append(data)

    # 2. Grade with Gemini Vision
    ai_report = grade_with_gemini(image_bytes_list, description)

    condition_score = ai_report.get("condition_score", 70)
    condition_grade = ai_report.get("grade", "B")

    # 3. Calculate warranty
    try:
        warranty_info = calculate_warranty_info(purchase_date, initial_warranty_days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4. Build product data for CatBoost
    missing_acc = "Yes" if ai_report.get("missing_accessories", False) else "No"

    product_data = {
        "product_category": product_category,
        "product_name": product_name,
        "brand": brand,
        "current_market_price": current_market_price,
        "purchase_price": purchase_price,
        "purchase_age_days": warranty_info["purchase_age_days"],
        "initial_warranty_days": initial_warranty_days,
        "warranty_left_days": warranty_info["warranty_left_days"],
        "condition_score": condition_score,
        "condition_grade": condition_grade,
        "scratch_severity": ai_report.get("scratch_severity", 0),
        "dent_severity": ai_report.get("dent_severity", 0),
        "crack_severity": ai_report.get("crack_severity", 0),
        "usage_severity": ai_report.get("usage_severity", 0),
        "missing_accessories": missing_acc,
        "seller_description": description,
    }

    # 5. Predict resale price
    pricing_result = predict_resale_price(product_data)

    # 6. Check warranty eligibility
    eligible = warranty_info["eligible_for_resale"]

    return {
        "success": True,
        "eligible_for_resale": eligible,
        "decision": "APPROVE_FOR_RESALE" if eligible and condition_grade not in ["Reject", "D"] else "REJECT_FOR_RESALE",
        "recommended_listing_price": pricing_result["predicted_resale_price"],
        "currency": "INR",
        "prediction": {
            "predicted_resale_price": pricing_result["predicted_resale_price"],
            "confidence_score": pricing_result["confidence_score"],
            "price_percentage_of_market": round((pricing_result["predicted_resale_price"] / current_market_price) * 100, 2) if current_market_price else None,
            "top_positive_factors": pricing_result.get("top_positive_factors", []),
            "top_negative_factors": pricing_result.get("top_negative_factors", []),
            "raw_shap_values": pricing_result.get("shap_values", {})
        },
        "warranty_policy": warranty_info,
        "ai_grading_report": {
            "condition_score": condition_score,
            "condition_grade": condition_grade,
            "gemini_report": {
                "detected_defects": ai_report.get("detected_defects", []),
                "scratch_severity": ai_report.get("scratch_severity", 0),
                "dent_severity": ai_report.get("dent_severity", 0),
                "crack_severity": ai_report.get("crack_severity", 0),
                "usage_severity": ai_report.get("usage_severity", 0),
                "packaging_damage": 0,
                "missing_accessories": ai_report.get("missing_accessories", False),
                "ai_condition_score": condition_score,
                "ai_recommended_grade": condition_grade,
                "inspection_summary": ai_report.get("inspection_summary", ""),
                "buyer_trust_report": ai_report.get("buyer_trust_report", "")
            }
        },
        "product_data_used": product_data,
        "warranty_offered": None,
        "ai_grading_source": ai_report.get("ai_source", "gemini"),
        "ai_pricing_source": pricing_result.get("ai_source", "unknown")
    }
