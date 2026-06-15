# =========================================================
# AI Pricing Module — CatBoost Resale Price Prediction
# Loads pre-trained inference engine with SHAP explainability
# =========================================================

import sys
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import date, datetime

logger = logging.getLogger("ai-pricing")

# Pre-trained inference engine (loaded at startup)
_inference_engine = None
_pricing_available = False

ARTIFACT_DIR = Path(__file__).parent.parent / "ai_artifacts"
INFERENCE_ENGINE_PATH = ARTIFACT_DIR / "resale_price_inference_engine.pkl"
TRAINING_MODULE_PATH = ARTIFACT_DIR / "train_resale_price_model.py"


def init_pricing_model() -> bool:
    """Load the pre-trained CatBoost inference engine."""
    global _inference_engine, _pricing_available

    if not INFERENCE_ENGINE_PATH.exists():
        logger.warning(f"Inference engine not found at {INFERENCE_ENGINE_PATH} — AI pricing disabled")
        return False

    try:
        if str(ARTIFACT_DIR) not in sys.path:
            sys.path.insert(0, str(ARTIFACT_DIR))

        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if module == "__main__":
                    import train_resale_price_model
                    return getattr(train_resale_price_model, name)
                return super().find_class(module, name)

        with open(INFERENCE_ENGINE_PATH, "rb") as f:
            _inference_engine = CustomUnpickler(f).load()

        _pricing_available = True
        logger.info("✅ CatBoost resale pricing model loaded successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to load pricing model (non-fatal): {e}")
        return False


def parse_date_string(date_string: str) -> date:
    """Parse various date formats into a date object."""
    formats = ["%Y-%m-%d", "%d %b %Y", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_string}")


def calculate_warranty_info(
    purchase_date: str,
    initial_warranty_days: int,
) -> Dict[str, Any]:
    """Calculate age and remaining warranty from purchase date."""
    purchase_dt = parse_date_string(purchase_date)
    today = date.today()

    purchase_age_days = max(0, (today - purchase_dt).days)
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


def predict_resale_price(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict resale price using the CatBoost model.
    
    Required keys in product_data:
        product_category, brand, current_market_price, purchase_price,
        purchase_age_days, initial_warranty_days, warranty_left_days,
        condition_score, condition_grade, scratch_severity, dent_severity,
        crack_severity, usage_severity, missing_accessories
    
    Returns:
        predicted_resale_price, confidence_score, top_positive_factors,
        top_negative_factors, shap_values
    """
    if not _pricing_available or _inference_engine is None:
        return _fallback_pricing(product_data)

    try:
        result = _inference_engine.explain_prediction(product_data)
        
        original_price = float(product_data.get("purchase_price", 0) or product_data.get("original_price", 0))
        predicted = float(result["predicted_resale_price"])
        
        # Cap resale price at 95% of original price to prevent unrealistic appreciation
        if original_price > 0 and predicted > (original_price * 0.95):
            predicted = original_price * 0.95
            
        return {
            "predicted_resale_price": round(predicted, 2),
            "confidence_score": result["confidence_score"],
            "top_positive_factors": result.get("top_positive_factors", []),
            "top_negative_factors": result.get("top_negative_factors", []),
            "shap_values": result.get("shap_values", {}),
            "ai_source": "catboost"
        }
    except Exception as e:
        logger.exception("CatBoost prediction failed, using fallback")
        return _fallback_pricing(product_data)


def _fallback_pricing(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple rule-based fallback when CatBoost is unavailable."""
    original_price = float(product_data.get("purchase_price", 0) or product_data.get("original_price", 0))
    condition_score = float(product_data.get("condition_score", 70))

    # Simple depreciation model
    condition_factor = condition_score / 100.0
    age_days = int(product_data.get("purchase_age_days", 180))
    age_factor = max(0.3, 1.0 - (age_days / 730.0))  # 2 year depreciation

    predicted = original_price * condition_factor * age_factor * 0.7
    predicted = max(100, round(predicted, 2))

    return {
        "predicted_resale_price": predicted,
        "confidence_score": 45.0,
        "top_positive_factors": ["Basic rule-based estimate"],
        "top_negative_factors": ["AI model unavailable — using simplified calculation"],
        "shap_values": {},
        "ai_source": "fallback_rules"
    }
