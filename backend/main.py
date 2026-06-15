# =========================================================
# Second Life Commerce — FastAPI Backend
# Main application with CORS, model loading, route mounting
# =========================================================

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ── Force local model cache to fix D:\ drive error ────────
os.environ["HF_HOME"] = os.path.join(os.getcwd(), ".hf_cache")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(os.getcwd(), ".hf_cache")
os.environ["TORCH_HOME"] = os.path.join(os.getcwd(), ".hf_cache")

# ── Configure logging ─────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("second-life")

# ── Model status tracking ─────────────────────────────────
model_status = {
    "clip": False,
    "xgboost": False,
    "sentence_transformer": False,
    "review_index": False,
    "gemini_vision": False,
    "catboost_pricing": False,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: Load all ML models.
    Shutdown: Cleanup.
    """
    logger.info("=" * 60)
    logger.info("  SECOND LIFE COMMERCE — Starting API Server")
    logger.info("=" * 60)

    # 1. Load CLIP
    try:
        from models.grading import load_clip_model
        model_status["clip"] = load_clip_model()
    except Exception as e:
        logger.error(f"CLIP load failed (non-fatal): {e}")

    # 2. Train XGBoost
    try:
        from models.pricing import train_pricing_model
        model_status["xgboost"] = train_pricing_model()
    except Exception as e:
        logger.error(f"XGBoost training failed (non-fatal): {e}")

    # 3. Load Sentence Transformer
    try:
        from models.reviews import load_review_model, build_review_index
        model_status["sentence_transformer"] = load_review_model()

        # 4. Build review index
        if model_status["sentence_transformer"]:
            model_status["review_index"] = build_review_index()
    except Exception as e:
        logger.error(f"Sentence Transformer load failed (non-fatal): {e}")

    # 5. Load Gemini Vision (AI Grading)
    try:
        from models.ai_grading import init_gemini
        model_status["gemini_vision"] = init_gemini()
    except Exception as e:
        logger.error(f"Gemini Vision init failed (non-fatal): {e}")

    # 6. Load CatBoost Pricing Model
    try:
        from models.ai_pricing import init_pricing_model
        model_status["catboost_pricing"] = init_pricing_model()
    except Exception as e:
        logger.error(f"CatBoost pricing init failed (non-fatal): {e}")

    logger.info("-" * 60)
    logger.info(f"  Models loaded: {sum(model_status.values())}/{len(model_status)}")
    for name, loaded in model_status.items():
        logger.info(f"    {'✅' if loaded else '❌'} {name}")
    logger.info("-" * 60)
    logger.info("  Second Life Commerce API ready on port 8000")
    logger.info("=" * 60)

    yield  # App is running

    logger.info("Shutting down Second Life Commerce API...")


# ── Create FastAPI app ────────────────────────────────────
app = FastAPI(
    title="Second Life Commerce API",
    description="AI-powered returns and resale platform for Amazon India",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS — allow React frontend ──────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # CRA dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Mount routes ──────────────────────────────────────────
from routes.grade import router as grade_router
from routes.price import router as price_router
from routes.listing import router as listing_router
from routes.reviews import router as reviews_router
from routes.returns import router as returns_router
from routes.resale import router as resale_router
from routes.seller import router as seller_router
from routes.ai_resale import router as ai_resale_router

app.include_router(grade_router, tags=["Grading"])
app.include_router(price_router, tags=["Pricing"])
app.include_router(listing_router, tags=["Listing"])
app.include_router(reviews_router, tags=["Reviews"])
app.include_router(returns_router, tags=["Returns"])
app.include_router(resale_router, tags=["Resale"])
app.include_router(seller_router, tags=["Seller"])
app.include_router(ai_resale_router, tags=["AI Resale"])


from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Product, Order

@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """Check API, DB, and model status."""
    db_status = True
    try:
        db.execute("SELECT 1")
    except Exception:
        db_status = False

    return {
        "status": "ok",
        "database_connected": db_status,
        "models_loaded": all(model_status.values()),
        "models": model_status,
    }


@app.get("/api/demo/products")
async def get_demo_products(db: Session = Depends(get_db)):
    """Return all products from DB for frontend."""
    products = db.query(Product).all()
    # Serialize to match the expected format
    data = []
    for p in products:
        data.append({
            "product_id": p.product_id,
            "name": p.name,
            "category": p.category,
            "original_price": p.original_price,
            "image_url": p.image_url,
            "is_second_life": p.is_second_life,
            "second_life_grade": p.second_life_grade,
            "second_life_price": p.second_life_price
        })
    return {
        "status": "success",
        "data": data,
    }

@app.get("/api/orders/me")
async def get_my_orders(db: Session = Depends(get_db)):
    """Return past orders for the mock user."""
    orders = db.query(Order).filter(Order.user_id == "user_123").all()
    data = []
    for o in orders:
        data.append({
            "order_id": o.order_id,
            "product_id": o.product.product_id,
            "product_name": o.product.name,
            "product_category": o.product.category,
            "original_price": o.product.original_price,
            "image_url": o.product.image_url,
            "purchase_date": o.purchase_date,
            "warranty_months": o.warranty_months,
            "weight_kg": o.weight_kg,
            "status": o.status,
            "return_eligible": o.return_eligible,
            "resell_eligible": o.resell_eligible
        })
    return {
        "status": "success",
        "data": data,
    }
