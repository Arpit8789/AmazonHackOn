import sys
import train_resale_price_model as training_module

# Fix pickle issue because model was trained when file ran as __main__
sys.modules["__main__"].ResalePriceInferenceEngine = training_module.ResalePriceInferenceEngine
sys.modules["__main__"].FeatureEngineer = training_module.FeatureEngineer
sys.modules["__main__"].safe_divide = training_module.safe_divide
sys.modules["__main__"].get_transformed_feature_names = training_module.get_transformed_feature_names

def add_business_warranty_reason(product_data, final_result):
    initial = product_data.get("initial_warranty_days", 0)
    left = product_data.get("warranty_left_days", 0)

    warranty_ratio = left / initial if initial > 0 else 0

    if warranty_ratio <= 0:
        final_result["top_negative_factors"].append(
            "Warranty has expired, reducing buyer trust"
        )
    elif warranty_ratio < 0.25:
        final_result["top_negative_factors"].append(
            "Very limited warranty remaining reduced resale value"
        )
    elif warranty_ratio >= 0.5:
        final_result["top_positive_factors"].append(
            "Strong warranty coverage increased buyer trust"
        )

    final_result["warranty_ratio"] = round(warranty_ratio * 100, 2)
    return final_result

def make_user_friendly_explanation(result):
    positive_map = {
        "condition_score": "High condition score increased resale value",
        "condition_squared": "Excellent overall condition strongly increased value",
        "warranty_left_days": "Remaining warranty increased buyer trust",
        "premium_brand_flag": "Premium brand improved resale demand",
        "high_value_product_flag": "High-value product category retained better resale value",
        "current_market_price": "Higher current market price increased resale estimate",
        "market_price_log": "Strong current market price supported resale value",
        "condition_grade_A": "Grade A condition improved resale value",
        "excellent_condition_flag": "Excellent condition improved buyer confidence"
    }

    negative_map = {
        "purchase_age_days": "Older product age reduced resale value",
        "age_years": "Longer usage period reduced resale value",
        "age_log": "Product age caused depreciation",
        "scratch_severity": "Visible scratches reduced resale value",
        "dent_severity": "Dents reduced resale value",
        "crack_severity": "Cracks reduced resale value significantly",
        "weighted_defect_score": "Overall damage reduced resale value",
        "missing_accessories_flag": "Missing accessories reduced resale value",
        "expired_warranty_flag": "Expired warranty reduced buyer trust",
        "price_retention_ratio": "Lower value retention reduced resale estimate"
    }

    positives = []
    negatives = []

    for item in result["top_positive_factors"]:
        key = item.split(":")[0].replace("num__", "").replace("cat__", "")
        for k, msg in positive_map.items():
            if k in key:
                positives.append(msg)
                break

    for item in result["top_negative_factors"]:
        key = item.split(":")[0].replace("num__", "").replace("cat__", "")
        for k, msg in negative_map.items():
            if k in key:
                negatives.append(msg)
                break

    return {
        "predicted_resale_price": result["predicted_resale_price"],
        "confidence_score": result["confidence_score"],
        "top_positive_factors": list(dict.fromkeys(positives))[:4],
        "top_negative_factors": list(dict.fromkeys(negatives))[:4],
        "raw_shap_values": result["shap_values"]
    }

def business_explanation(product_data, model_result):
    positive = []
    negative = []

    condition = product_data.get("condition_score", 0)
    age_days = product_data.get("purchase_age_days", 0)
    initial_warranty = product_data.get("initial_warranty_days", 0)
    warranty_left = product_data.get("warranty_left_days", 0)

    scratch = product_data.get("scratch_severity", 0)
    dent = product_data.get("dent_severity", 0)
    crack = product_data.get("crack_severity", 0)
    usage = product_data.get("usage_severity", 0)

    brand = product_data.get("brand", "")
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

    if not positive:
        positive.append("Product still has resale potential based on market value")

    if not negative:
        negative.append("No major negative factors detected")

    return {
        "predicted_resale_price": model_result["predicted_resale_price"],
        "confidence_score": model_result["confidence_score"],
        "top_positive_factors": positive[:5],
        "top_negative_factors": negative[:5],
        "raw_shap_values": model_result.get("shap_values", {})
    }

from train_resale_price_model import explain_prediction

# product_data = {
#     "product_category": "Mobile Phones",
#     "brand": "Apple",
#     "current_market_price": 70000,
#     "purchase_price": 80000,
#     "purchase_age_days": 365,
#     "initial_warranty_days": 365,
#     "warranty_left_days": 45,
#     "condition_score": 88,
#     "condition_grade": "A",
#     "scratch_severity": 2,
#     "dent_severity": 0,
#     "crack_severity": 0,
#     "usage_severity": 3,
#     "missing_accessories": "No"
# }

demo_products = [
    {
        "product_category": "Laptops",
        "brand": "Dell",
        "current_market_price": 85000,
        "purchase_price": 95000,
        "purchase_age_days": 540,
        "initial_warranty_days": 730,
        "warranty_left_days": 190,
        "condition_score": 81,
        "condition_grade": "B",
        "scratch_severity": 3,
        "dent_severity": 1,
        "crack_severity": 0,
        "usage_severity": 4,
        "missing_accessories": "No"
    },
    {
        "product_category": "Headphones",
        "brand": "Sony",
        "current_market_price": 18000,
        "purchase_price": 22000,
        "purchase_age_days": 240,
        "initial_warranty_days": 365,
        "warranty_left_days": 100,
        "condition_score": 90,
        "condition_grade": "A",
        "scratch_severity": 1,
        "dent_severity": 0,
        "crack_severity": 0,
        "usage_severity": 2,
        "missing_accessories": "No"
    },
    {
        "product_category": "Televisions",
        "brand": "Samsung",
        "current_market_price": 60000,
        "purchase_price": 72000,
        "purchase_age_days": 900,
        "initial_warranty_days": 365,
        "warranty_left_days": 0,
        "condition_score": 58,
        "condition_grade": "C",
        "scratch_severity": 6,
        "dent_severity": 4,
        "crack_severity": 3,
        "usage_severity": 7,
        "missing_accessories": "Yes"
    },
    {
        "product_category": "Refrigerators",
        "brand": "LG",
        "current_market_price": 42000,
        "purchase_price": 50000,
        "purchase_age_days": 720,
        "initial_warranty_days": 1095,
        "warranty_left_days": 375,
        "condition_score": 84,
        "condition_grade": "B",
        "scratch_severity": 2,
        "dent_severity": 2,
        "crack_severity": 0,
        "usage_severity": 4,
        "missing_accessories": "No"
    },
    {
        "product_category": "Washing Machines",
        "brand": "Bosch",
        "current_market_price": 38000,
        "purchase_price": 45000,
        "purchase_age_days": 610,
        "initial_warranty_days": 730,
        "warranty_left_days": 120,
        "condition_score": 76,
        "condition_grade": "B",
        "scratch_severity": 3,
        "dent_severity": 2,
        "crack_severity": 0,
        "usage_severity": 5,
        "missing_accessories": "No"
    },
    {
        "product_category": "Furniture",
        "brand": "Ikea",
        "current_market_price": 25000,
        "purchase_price": 32000,
        "purchase_age_days": 1100,
        "initial_warranty_days": 365,
        "warranty_left_days": 0,
        "condition_score": 68,
        "condition_grade": "C",
        "scratch_severity": 5,
        "dent_severity": 4,
        "crack_severity": 2,
        "usage_severity": 6,
        "missing_accessories": "Yes"
    },
    {
        "product_category": "Tablets",
        "brand": "Apple",
        "current_market_price": 55000,
        "purchase_price": 65000,
        "purchase_age_days": 300,
        "initial_warranty_days": 365,
        "warranty_left_days": 65,
        "condition_score": 87,
        "condition_grade": "A",
        "scratch_severity": 1,
        "dent_severity": 0,
        "crack_severity": 0,
        "usage_severity": 3,
        "missing_accessories": "No"
    },
    {
        "product_category": "Smart Watches",
        "brand": "Samsung",
        "current_market_price": 28000,
        "purchase_price": 34000,
        "purchase_age_days": 430,
        "initial_warranty_days": 365,
        "warranty_left_days": 0,
        "condition_score": 72,
        "condition_grade": "C",
        "scratch_severity": 4,
        "dent_severity": 1,
        "crack_severity": 1,
        "usage_severity": 5,
        "missing_accessories": "Yes"
    }
]

PREMIUM_BRANDS = {
    "Apple", "Samsung", "Sony", "Dell", "HP", "Lenovo", "LG",
    "Bosch", "Whirlpool", "OnePlus", "Google", "Microsoft",
    "Asus", "JBL", "Bose", "Panasonic", "Haier", "Xiaomi", "Ikea"
}

for product in demo_products:

    # Raw SHAP explanation
    raw_result = explain_prediction(
        product,
        artifact_dir="artifacts"
    )

    # Business-friendly explanation
    final_result = business_explanation(
        product,
        raw_result
    )

    print("\n================================")
    print(product["product_category"], "-", product["brand"])

    print("\nPredicted Price:")
    print("₹", final_result["predicted_resale_price"])

    print("\nConfidence:")
    print(final_result["confidence_score"], "%")

    print("\nPositive Factors:")
    for factor in final_result["top_positive_factors"]:
        print("✓", factor)

    print("\nNegative Factors:")
    for factor in final_result["top_negative_factors"]:
        print("✗", factor)

    print("\n================================")

# raw_result = explain_prediction(product_data, artifact_dir="artifacts")
# final_result = make_user_friendly_explanation(raw_result)
# final_result = add_business_warranty_reason(product_data, final_result)


# print(final_result)

# print("\nPredicted Resale Price:")
# print("₹", final_result["predicted_resale_price"])

# print("\nConfidence Score:")
# print(final_result["confidence_score"], "%")

# print("\nTop Positive Factors:")
# for factor in final_result["top_positive_factors"]:
#     print("+", factor)

# print("\nTop Negative Factors:")
# for factor in final_result["top_negative_factors"]:
#     print("-", factor)

# print("\nFull Output:")
# print(final_result)