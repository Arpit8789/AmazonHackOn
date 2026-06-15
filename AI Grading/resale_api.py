"""
resale_api.py

FastAPI API for Amazon Second Life Commerce resale pricing.

Flow:
1. Receives product images + product/order details.
2. Calls Gemini Vision/Vertex AI to grade condition.
3. Calculates purchase_age_days and warranty_left_days automatically.
4. Checks resale warranty eligibility:
      warranty_left_days >= max(60, 25% of initial_warranty_days)
5. Calls trained resale price model.
6. Returns price + confidence + AI grading + business explanation.

Run:
    uvicorn resale_api:app --reload --host 0.0.0.0 --port 8000

Swagger UI:
    http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import sys
import json
import pickle
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

from google import genai
from google.genai import types
from google.oauth2 import service_account

# Needed for loading pickle created during training.
import train_resale_price_model as training_module

sys.modules["__main__"].ResalePriceInferenceEngine = training_module.ResalePriceInferenceEngine
sys.modules["__main__"].FeatureEngineer = training_module.FeatureEngineer
sys.modules["__main__"].safe_divide = training_module.safe_divide
sys.modules["__main__"].get_transformed_feature_names = training_module.get_transformed_feature_names

SERVICE_ACCOUNT_FILE = "service-account.json"
PROJECT_ID = "datatech-497104"
LOCATION = "us-central1"
GEMINI_MODEL = "gemini-2.5-flash"

ARTIFACT_DIR = Path("artifacts")
INFERENCE_ENGINE_PATH = ARTIFACT_DIR / "resale_price_inference_engine.pkl"
MAX_IMAGES = 3

PREMIUM_BRANDS = {
    "Apple", "Samsung", "Sony", "Dell", "HP", "Lenovo", "LG",
    "Bosch", "Whirlpool", "OnePlus", "Google", "Microsoft",
    "Asus", "JBL", "Bose", "Panasonic", "Haier", "Xiaomi", "Ikea"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("resale_api")

app = FastAPI(
    title="Amazon Second Life Commerce API",
    description="AI product grading + resale price prediction + explainability API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_client = None
inference_engine = None


@app.on_event("startup")
def startup_event():
    global gemini_client, inference_engine

    logger.info("Starting API...")

    if not Path(SERVICE_ACCOUNT_FILE).exists():
        raise RuntimeError(
            f"Missing {SERVICE_ACCOUNT_FILE}. Place your Google service account JSON in project root."
        )

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    gemini_client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        credentials=credentials
    )

    if not INFERENCE_ENGINE_PATH.exists():
        raise RuntimeError(
            f"Missing model artifact: {INFERENCE_ENGINE_PATH}. Train the model first."
        )

    with open(INFERENCE_ENGINE_PATH, "rb") as f:
        inference_engine = pickle.load(f)

    logger.info("Gemini client and resale model loaded successfully.")


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def uploaded_image_to_part(uploaded_file: UploadFile) -> types.Part:
    image_bytes = uploaded_file.file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=70)
    return types.Part.from_bytes(data=buffer.getvalue(), mime_type="image/jpeg")


def fallback_report(message: str = "Unable to parse AI response.") -> Dict[str, Any]:
    return {
        "detected_defects": [],
        "scratch_severity": 0,
        "dent_severity": 0,
        "crack_severity": 0,
        "usage_severity": 0,
        "packaging_damage": 0,
        "missing_accessories": False,
        "ai_condition_score": 0,
        "ai_recommended_grade": "Unknown",
        "inspection_summary": message,
        "buyer_trust_report": "Could not generate a reliable trust report."
    }


def clean_json_response(text: str) -> Dict[str, Any]:
    try:
        text = text.strip().replace("```json", "").replace("```", "").strip()
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        return json.loads(text)
    except Exception:
        logger.exception("Gemini returned invalid JSON. Raw response: %s", text)
        return fallback_report("Gemini returned incomplete or invalid JSON.")


def calculate_score(report: Dict[str, Any]) -> int:
    score = 100
    score -= safe_int(report.get("scratch_severity", 0)) * 3
    score -= safe_int(report.get("dent_severity", 0)) * 4
    score -= safe_int(report.get("crack_severity", 0)) * 8
    score -= safe_int(report.get("usage_severity", 0)) * 3
    score -= safe_int(report.get("packaging_damage", 0)) * 2
    if report.get("missing_accessories", False):
        score -= 15
    return max(0, min(100, round(score)))


def assign_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "Reject"


def parse_date(date_string: str, field_name: str) -> date:
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}. Use YYYY-MM-DD format.")


def calculate_age_and_warranty(
    purchase_date: str,
    initial_warranty_days: int,
    as_of_date: Optional[str] = None
) -> Dict[str, Any]:
    purchase_dt = parse_date(purchase_date, "purchase_date")
    today = parse_date(as_of_date, "as_of_date") if as_of_date else date.today()

    if purchase_dt > today:
        raise HTTPException(status_code=400, detail="purchase_date cannot be in the future.")

    purchase_age_days = (today - purchase_dt).days
    warranty_left_days = max(0, initial_warranty_days - purchase_age_days)
    required_warranty_days = max(60, int(0.25 * initial_warranty_days))
    eligible_for_resale = warranty_left_days >= required_warranty_days

    return {
        "purchase_age_days": purchase_age_days,
        "warranty_left_days": warranty_left_days,
        "required_warranty_days": required_warranty_days,
        "eligible_for_resale": eligible_for_resale,
        "warranty_ratio": round(warranty_left_days / initial_warranty_days, 4) if initial_warranty_days > 0 else 0
    }


def call_gemini(uploaded_images: List[UploadFile], description: str) -> Dict[str, Any]:
    prompt = f"""
You are an expert product condition inspector for an Amazon-style resale marketplace.

Seller description:
\"{description}\"

Analyze the product images.

Return ONLY valid JSON.
Do not use markdown.
Do not write explanation outside JSON.
Do not add trailing commas.
Use only numbers for severity fields.
Severity values must be integers from 0 to 10.
Maximum 3 detected defects.
Keep summaries short.

JSON format:
{{
  "detected_defects": [
    {{
      "type": "scratch",
      "severity": 0,
      "location": "front side",
      "confidence": 0
    }}
  ],
  "scratch_severity": 0,
  "dent_severity": 0,
  "crack_severity": 0,
  "usage_severity": 0,
  "packaging_damage": 0,
  "missing_accessories": false,
  "ai_condition_score": 0,
  "ai_recommended_grade": "A",
  "inspection_summary": "short summary",
  "buyer_trust_report": "short buyer-facing report"
}}
"""
    try:
        image_parts = [uploaded_image_to_part(img) for img in uploaded_images[:MAX_IMAGES]]
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2000,
                response_mime_type="application/json"
            )
        )
        report = clean_json_response(response.text.strip())

        for key in ["scratch_severity", "dent_severity", "crack_severity", "usage_severity", "packaging_damage"]:
            report[key] = max(0, min(10, safe_int(report.get(key, 0))))
        report["ai_condition_score"] = max(0, min(100, safe_int(report.get("ai_condition_score", 0))))
        report["missing_accessories"] = bool(report.get("missing_accessories", False))
        return report
    except Exception as e:
        logger.exception("Gemini API call failed.")
        return fallback_report(f"Gemini API call failed: {str(e)}")


def business_explanation(product_data: Dict[str, Any], model_result: Dict[str, Any]) -> Dict[str, Any]:
    positive = []
    negative = []

    condition = safe_float(product_data.get("condition_score", 0))
    age_days = safe_int(product_data.get("purchase_age_days", 0))
    initial_warranty = safe_int(product_data.get("initial_warranty_days", 0))
    warranty_left = safe_int(product_data.get("warranty_left_days", 0))
    scratch = safe_int(product_data.get("scratch_severity", 0))
    dent = safe_int(product_data.get("dent_severity", 0))
    crack = safe_int(product_data.get("crack_severity", 0))
    usage = safe_int(product_data.get("usage_severity", 0))
    brand = str(product_data.get("brand", ""))
    current_market_price = safe_float(product_data.get("current_market_price", 0))
    purchase_price = safe_float(product_data.get("purchase_price", 0))
    missing_accessories = str(product_data.get("missing_accessories", "No")).lower()
    warranty_ratio = warranty_left / initial_warranty if initial_warranty > 0 else 0

    if condition >= 85:
        positive.append("Excellent condition increased resale value")
    elif condition >= 70:
        positive.append("Good usable condition supported resale value")
    elif condition < 60:
        negative.append("Low condition score reduced resale value")

    if brand in PREMIUM_BRANDS:
        positive.append("Premium brand improved buyer trust and resale demand")

    if warranty_ratio >= 0.50:
        positive.append("Strong warranty coverage increased buyer confidence")
    elif warranty_ratio > 0.25:
        positive.append("Some warranty is still available")
    elif warranty_ratio > 0:
        negative.append("Very limited warranty remaining reduced buyer trust")
    else:
        negative.append("Expired warranty reduced buyer trust")

    if age_days <= 180:
        positive.append("Recently purchased product retained higher value")
    elif age_days > 365:
        negative.append("Product age caused depreciation")

    if scratch >= 4:
        negative.append("Visible scratches reduced resale value")
    if dent >= 3:
        negative.append("Dents reduced resale value")
    if crack > 0:
        negative.append("Cracks significantly reduced resale value")
    if usage >= 6:
        negative.append("Heavy usage reduced resale value")

    if missing_accessories in ["yes", "true", "1"]:
        negative.append("Missing accessories reduced resale value")

    if current_market_price > 0 and purchase_price > 0:
        if current_market_price >= purchase_price * 0.80:
            positive.append("Current market price is still strong")
        elif current_market_price < purchase_price * 0.60:
            negative.append("Market price has depreciated significantly")

    if not positive:
        positive.append("Product still has resale potential based on market value")
    if not negative:
        negative.append("No major negative factors detected")

    return {
        "predicted_resale_price": model_result["predicted_resale_price"],
        "confidence_score": model_result["confidence_score"],
        "price_percentage_of_market": model_result.get("price_percentage_of_market"),
        "top_positive_factors": positive[:5],
        "top_negative_factors": negative[:5],
        "raw_shap_values": model_result.get("shap_values", {})
    }


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    gemini_loaded: bool


@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "model_loaded": inference_engine is not None,
        "gemini_loaded": gemini_client is not None
    }


@app.post("/predict-resale")
async def predict_resale(
    images: List[UploadFile] = File(...),
    description: str = Form(...),
    product_category: str = Form(...),
    brand: str = Form(...),
    product_name: str = Form("Unknown Product"),
    purchase_price: float = Form(...),
    current_market_price: float = Form(...),
    purchase_date: str = Form(...),
    initial_warranty_days: int = Form(...),
    warranty_offered: Optional[str] = Form(None),
    as_of_date: Optional[str] = Form(None),
):
    if not images:
        raise HTTPException(status_code=400, detail="At least one image is required.")
    if len(images) > MAX_IMAGES:
        images = images[:MAX_IMAGES]
    if purchase_price <= 0 or current_market_price <= 0:
        raise HTTPException(status_code=400, detail="purchase_price and current_market_price must be positive.")
    if initial_warranty_days <= 0:
        raise HTTPException(status_code=400, detail="initial_warranty_days must be positive.")

    warranty_info = calculate_age_and_warranty(purchase_date, initial_warranty_days, as_of_date)
    ai_report = call_gemini(images, description)
    final_score = calculate_score(ai_report)
    final_grade = assign_grade(final_score)
    missing_accessories_value = "Yes" if ai_report.get("missing_accessories", False) else "No"

    product_data = {
        "product_category": product_category,
        "product_name": product_name,
        "brand": brand,
        "current_market_price": current_market_price,
        "purchase_price": purchase_price,
        "purchase_age_days": warranty_info["purchase_age_days"],
        "initial_warranty_days": initial_warranty_days,
        "warranty_left_days": warranty_info["warranty_left_days"],
        "condition_score": final_score,
        "condition_grade": final_grade,
        "scratch_severity": safe_int(ai_report.get("scratch_severity", 0)),
        "dent_severity": safe_int(ai_report.get("dent_severity", 0)),
        "crack_severity": safe_int(ai_report.get("crack_severity", 0)),
        "usage_severity": safe_int(ai_report.get("usage_severity", 0)),
        "missing_accessories": missing_accessories_value,
        "seller_description": description,
    }

    if not warranty_info["eligible_for_resale"]:
        return {
            "success": True,
            "eligible_for_resale": False,
            "decision": "REJECT_FOR_RESALE",
            "reason": (
                f"Warranty left is {warranty_info['warranty_left_days']} days, "
                f"but minimum required warranty is {warranty_info['required_warranty_days']} days."
            ),
            "warranty_policy": {
                "minimum_required_warranty_days": warranty_info["required_warranty_days"],
                "warranty_left_days": warranty_info["warranty_left_days"],
                "warranty_ratio": warranty_info["warranty_ratio"],
                "rule": "warranty_left_days >= max(60, 0.25 * initial_warranty_days)"
            },
            "ai_grading_report": {
                "condition_score": final_score,
                "condition_grade": final_grade,
                "gemini_report": ai_report
            },
            "product_data_used": product_data
        }

    model_result = inference_engine.explain_prediction(product_data)
    final_result = business_explanation(product_data, model_result)

    return {
        "success": True,
        "eligible_for_resale": True,
        "decision": "APPROVE_FOR_RESALE",
        "recommended_listing_price": round(final_result["predicted_resale_price"], 2),
        "currency": "INR",
        "prediction": final_result,
        "warranty_policy": {
            "minimum_required_warranty_days": warranty_info["required_warranty_days"],
            "warranty_left_days": warranty_info["warranty_left_days"],
            "warranty_ratio": warranty_info["warranty_ratio"],
            "rule": "warranty_left_days >= max(60, 0.25 * initial_warranty_days)"
        },
        "ai_grading_report": {
            "condition_score": final_score,
            "condition_grade": final_grade,
            "gemini_report": ai_report
        },
        "product_data_used": product_data,
        "warranty_offered": warranty_offered
    }


@app.post("/predict-resale-without-images")
async def predict_resale_without_images(
    description: str = Form(...),
    product_category: str = Form(...),
    brand: str = Form(...),
    product_name: str = Form("Unknown Product"),
    purchase_price: float = Form(...),
    current_market_price: float = Form(...),
    purchase_date: str = Form(...),
    initial_warranty_days: int = Form(...),
    condition_score: int = Form(...),
    condition_grade: str = Form(...),
    scratch_severity: int = Form(0),
    dent_severity: int = Form(0),
    crack_severity: int = Form(0),
    usage_severity: int = Form(0),
    missing_accessories: str = Form("No"),
    as_of_date: Optional[str] = Form(None),
):
    warranty_info = calculate_age_and_warranty(purchase_date, initial_warranty_days, as_of_date)

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
        "scratch_severity": scratch_severity,
        "dent_severity": dent_severity,
        "crack_severity": crack_severity,
        "usage_severity": usage_severity,
        "missing_accessories": missing_accessories,
        "seller_description": description,
    }

    if not warranty_info["eligible_for_resale"]:
        return {
            "success": True,
            "eligible_for_resale": False,
            "decision": "REJECT_FOR_RESALE",
            "reason": (
                f"Warranty left is {warranty_info['warranty_left_days']} days, "
                f"but minimum required warranty is {warranty_info['required_warranty_days']} days."
            ),
            "warranty_policy": warranty_info,
            "product_data_used": product_data
        }

    model_result = inference_engine.explain_prediction(product_data)
    final_result = business_explanation(product_data, model_result)

    return {
        "success": True,
        "eligible_for_resale": True,
        "decision": "APPROVE_FOR_RESALE",
        "recommended_listing_price": round(final_result["predicted_resale_price"], 2),
        "currency": "INR",
        "prediction": final_result,
        "warranty_policy": warranty_info,
        "product_data_used": product_data
    }
