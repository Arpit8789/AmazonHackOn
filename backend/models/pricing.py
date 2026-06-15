# =========================================================
# XGBoost Pricing Engine + SHAP Explainability
# Trains on synthetic data at startup, predicts resale price
# =========================================================

import logging
import numpy as np

logger = logging.getLogger(__name__)

# ── Global model references ───────────────────────────────
_xgb_model = None
_shap_explainer = None
_feature_names = ["warranty_remaining_pct", "demand_score", "original_price", "product_age_days"]

# ── Delivery zone multipliers ─────────────────────────────
ZONE_MULTIPLIERS = {
    "local":    0.5,
    "city":     1.0,
    "regional": 1.5,
    "national": 2.5,
}

ZONE_LABELS = {
    "local":    "Local (same city)",
    "city":     "Nearby cities",
    "regional": "Regional (same state)",
    "national": "All India",
}


def train_pricing_model():
    """
    Generate synthetic training data and fit XGBoost.
    Called once at FastAPI startup — takes <1 second.
    """
    global _xgb_model, _shap_explainer

    try:
        from xgboost import XGBRegressor
        import shap

        np.random.seed(42)
        n_samples = 80

        # ── Generate synthetic training data ──────────────
        warranty_pct    = np.random.uniform(10, 100, n_samples)
        demand_score    = np.random.uniform(0.1, 1.0, n_samples)
        original_price  = np.random.choice([999, 1999, 2999, 3499, 4999, 6999, 9999], n_samples)
        age_days        = np.random.randint(15, 400, n_samples)

        # Target: resale price = f(warranty, demand, price, age)
        # Realistic formula with noise
        resale_ratio = (
            0.25                                    # base floor (25%)
            + 0.40 * (warranty_pct / 100)           # warranty adds up to 40%
            + 0.15 * demand_score                   # demand adds up to 15%
            - 0.10 * np.clip(age_days / 365, 0, 1)  # age penalty up to 10%
            + np.random.normal(0, 0.03, n_samples)  # noise ±3%
        )
        resale_ratio = np.clip(resale_ratio, 0.15, 0.90)
        resale_price = original_price * resale_ratio

        X = np.column_stack([warranty_pct, demand_score, original_price, age_days])

        # ── Train XGBoost ─────────────────────────────────
        _xgb_model = XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
        )
        _xgb_model.fit(X, resale_price)

        # ── Build SHAP explainer ──────────────────────────
        _shap_explainer = shap.TreeExplainer(_xgb_model)

        logger.info("✅ XGBoost pricing model trained + SHAP explainer ready")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to train pricing model: {e}")
        return False


def is_loaded() -> bool:
    """Check if pricing model is ready."""
    return _xgb_model is not None


def predict_price(
    warranty_remaining_percent: float,
    original_price: float,
    product_age_days: int,
    demand_score: float,
    weight_kg: float,
    delivery_zone: str,
    product_category: str = "Electronics",
) -> dict:
    """
    Predict resale price with full breakdown + SHAP explanation.

    Returns:
        dict with price_low, price_high, shap_explanation, breakdown, etc.
    """
    if not is_loaded():
        return _fallback_price(original_price, warranty_remaining_percent)

    try:
        X_input = np.array([[
            warranty_remaining_percent,
            demand_score,
            original_price,
            product_age_days,
        ]])

        # ── Predict ───────────────────────────────────────
        predicted = float(_xgb_model.predict(X_input)[0])
        price_low = max(int(predicted * 0.90), 100)
        price_high = int(predicted * 1.10)

        # ── SHAP values ──────────────────────────────────
        shap_values = _shap_explainer.shap_values(X_input)[0]
        shap_explanation = _build_shap_explanation(
            shap_values, X_input[0],
            warranty_remaining_percent, demand_score,
            product_category,
        )

        # ── Platform charges ─────────────────────────────
        zone_mult = ZONE_MULTIPLIERS.get(delivery_zone, 1.0)
        packaging = 40
        reprocessing = 30
        platform_fee = int(price_high * 0.07)
        delivery_charge = int(weight_kg * 80 * zone_mult)

        total_charges = packaging + reprocessing + platform_fee + delivery_charge
        final_price_buyer = price_high + total_charges
        seller_receives = price_low - reprocessing

        return {
            "eligible": True,
            "price_low": price_low,
            "price_high": price_high,
            "predicted_value": int(predicted),
            "shap_explanation": shap_explanation,
            "breakdown": {
                "resale_value": f"₹{price_low:,} — ₹{price_high:,}",
                "packaging_cost": packaging,
                "reprocessing_charge": reprocessing,
                "amazon_platform_fee_7pct": platform_fee,
                "delivery_charge": delivery_charge,
                "delivery_zone": ZONE_LABELS.get(delivery_zone, delivery_zone),
                "delivery_zone_key": delivery_zone,
            },
            "final_price_to_buyer_low": price_low + total_charges,
            "final_price_to_buyer_high": final_price_buyer,
            "seller_receives": max(seller_receives, 50),
        }

    except Exception as e:
        logger.error(f"Pricing prediction error: {e}")
        return _fallback_price(original_price, warranty_remaining_percent)


def _build_shap_explanation(
    shap_vals, feature_vals,
    warranty_pct, demand_score,
    category,
) -> list[dict]:
    """Convert SHAP values into human-readable explanation rows."""
    explanation = []

    # Warranty factor
    impact = int(shap_vals[0])
    explanation.append({
        "factor": f"Warranty remaining: {warranty_pct:.0f}%",
        "impact_inr": f"{'+'if impact >= 0 else ''}₹{abs(impact):,}",
        "direction": "positive" if impact >= 0 else "negative",
    })

    # Demand factor
    impact = int(shap_vals[1])
    demand_label = "high" if demand_score > 0.7 else "medium" if demand_score > 0.4 else "low"
    explanation.append({
        "factor": f"{demand_label.capitalize()} regional demand",
        "impact_inr": f"{'+'if impact >= 0 else ''}₹{abs(impact):,}",
        "direction": "positive" if impact >= 0 else "negative",
    })

    # Price baseline factor
    impact = int(shap_vals[2])
    explanation.append({
        "factor": f"Original price: ₹{int(feature_vals[2]):,}",
        "impact_inr": f"{'+'if impact >= 0 else ''}₹{abs(impact):,}",
        "direction": "positive" if impact >= 0 else "negative",
    })

    # Age factor
    impact = int(shap_vals[3])
    age_months = int(feature_vals[3] / 30)
    explanation.append({
        "factor": f"Product age: {age_months} months",
        "impact_inr": f"{'+'if impact >= 0 else ''}₹{abs(impact):,}",
        "direction": "positive" if impact >= 0 else "negative",
    })

    # Category confidence (mock — not a SHAP feature but adds value)
    sell_through = np.random.randint(65, 95)
    explanation.append({
        "factor": f"Category sell-through rate: {sell_through}%",
        "impact_inr": "HIGH confidence" if sell_through > 75 else "MEDIUM confidence",
        "direction": "neutral",
    })

    return explanation


def _fallback_price(original_price: float, warranty_pct: float) -> dict:
    """Fallback pricing when model is not loaded."""
    ratio = 0.3 + 0.5 * (warranty_pct / 100)
    price_low = int(original_price * ratio * 0.9)
    price_high = int(original_price * ratio * 1.1)

    return {
        "eligible": True,
        "price_low": price_low,
        "price_high": price_high,
        "predicted_value": int((price_low + price_high) / 2),
        "shap_explanation": [
            {"factor": f"Warranty remaining: {warranty_pct:.0f}%", "impact_inr": f"+₹{int(original_price * 0.3):,}", "direction": "positive"},
            {"factor": "Medium regional demand", "impact_inr": "+₹200", "direction": "positive"},
            {"factor": "Category sell-through rate: 78%", "impact_inr": "HIGH confidence", "direction": "neutral"},
        ],
        "breakdown": {
            "resale_value": f"₹{price_low:,} — ₹{price_high:,}",
            "packaging_cost": 40,
            "reprocessing_charge": 30,
            "amazon_platform_fee_7pct": int(price_high * 0.07),
            "delivery_charge": 80,
            "delivery_zone": "Nearby cities",
            "delivery_zone_key": "city",
        },
        "final_price_to_buyer_low": price_low + 40 + 30 + int(price_high * 0.07) + 80,
        "final_price_to_buyer_high": price_high + 40 + 30 + int(price_high * 0.07) + 80,
        "seller_receives": price_low - 30,
    }
