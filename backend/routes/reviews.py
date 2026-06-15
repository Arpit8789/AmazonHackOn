# =========================================================
# /api/reviews/ask — Multilingual Review QA Route
# =========================================================

from fastapi import APIRouter
from pydantic import BaseModel

from models.reviews import ask_question

router = APIRouter()


class ReviewQuestionRequest(BaseModel):
    product_id: str
    question: str
    language: str = ""  # optional hint: en, hi, hinglish


@router.post("/api/reviews/ask")
async def ask_review_question(req: ReviewQuestionRequest):
    """
    Answer a product question using semantic search over multilingual reviews.
    """
    result = ask_question(
        product_id=req.product_id,
        question=req.question,
        language_hint=req.language,
    )

    return {"status": "success", "data": result}
