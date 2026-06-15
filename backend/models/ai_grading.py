# =========================================================
# AI Grading Module — Gemini Vision Product Inspection
# Uses Vertex AI Gemini 2.5 Flash for defect detection
# Falls back to existing CLIP model if Gemini is unavailable
# =========================================================

import json
import logging
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

from PIL import Image

logger = logging.getLogger("ai-grading")

# Gemini client (initialized at startup)
_gemini_client = None
_gemini_available = False

GEMINI_MODEL = "gemini-2.5-flash"
MAX_IMAGES = 3


def init_gemini():
    """Initialize Gemini client using service account credentials."""
    global _gemini_client, _gemini_available

    sa_path = Path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", str(Path(__file__).parent.parent / "service-account.json")))
    if not sa_path.exists():
        logger.warning("service-account.json not found — Gemini grading disabled, using CLIP fallback")
        return False

    try:
        from google import genai
        from google.genai import types
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            str(sa_path),
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        _gemini_client = genai.Client(
            vertexai=True,
            project="datatech-497104",
            location="us-central1",
            credentials=credentials
        )
        _gemini_available = True
        logger.info("✅ Gemini Vision client initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Gemini init failed (non-fatal, using CLIP fallback): {e}")
        return False


def _image_bytes_to_part(image_bytes: bytes):
    """Convert raw image bytes to a Gemini-compatible Part."""
    from google.genai import types

    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=70)
    return types.Part.from_bytes(data=buffer.getvalue(), mime_type="image/jpeg")


def _clean_json_response(text: str) -> Dict[str, Any]:
    """Parse Gemini's JSON response, stripping markdown fences."""
    try:
        text = text.strip().replace("```json", "").replace("```", "").strip()
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        return json.loads(text)
    except Exception:
        logger.exception("Gemini returned invalid JSON. Raw: %s", text[:500])
        return _fallback_report("Gemini returned invalid JSON.")


def _fallback_report(message: str = "Unable to parse AI response.") -> Dict[str, Any]:
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


def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def calculate_condition_score(report: Dict[str, Any]) -> int:
    """Calculate a 0-100 condition score from the AI inspection report."""
    score = 100
    score -= _safe_int(report.get("scratch_severity", 0)) * 3
    score -= _safe_int(report.get("dent_severity", 0)) * 4
    score -= _safe_int(report.get("crack_severity", 0)) * 8
    score -= _safe_int(report.get("usage_severity", 0)) * 3
    score -= _safe_int(report.get("packaging_damage", 0)) * 2
    if report.get("missing_accessories", False):
        score -= 15
    return max(0, min(100, round(score)))


def assign_grade(score: int) -> str:
    """Assign a letter grade based on condition score."""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "Reject"


def grade_with_gemini(image_bytes_list: List[bytes], description: str = "") -> Dict[str, Any]:
    """
    Grade product condition using Gemini Vision.
    Returns: condition_score, grade, detected_defects, inspection_summary, etc.
    Falls back to CLIP if Gemini is unavailable.
    """
    if not _gemini_available or _gemini_client is None:
        logger.info("Gemini not available, falling back to CLIP grading")
        return _grade_with_clip_fallback(image_bytes_list)

    from google.genai import types

    prompt = f"""
You are an expert product condition inspector for an Amazon-style resale marketplace.

Seller description:
"{description}"

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
        image_parts = [_image_bytes_to_part(img) for img in image_bytes_list[:MAX_IMAGES]]
        response = _gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2000,
                response_mime_type="application/json"
            )
        )
        report = _clean_json_response(response.text.strip())

        # Sanitize severity values
        for key in ["scratch_severity", "dent_severity", "crack_severity", "usage_severity", "packaging_damage"]:
            report[key] = max(0, min(10, _safe_int(report.get(key, 0))))
        report["ai_condition_score"] = max(0, min(100, _safe_int(report.get("ai_condition_score", 0))))
        report["missing_accessories"] = bool(report.get("missing_accessories", False))

        # Calculate our own score and grade (more consistent than Gemini's)
        final_score = calculate_condition_score(report)
        final_grade = assign_grade(final_score)

        return {
            "condition_score": final_score,
            "grade": final_grade,
            "detected_defects": report.get("detected_defects", []),
            "inspection_summary": report.get("inspection_summary", ""),
            "buyer_trust_report": report.get("buyer_trust_report", ""),
            "scratch_severity": report["scratch_severity"],
            "dent_severity": report["dent_severity"],
            "crack_severity": report["crack_severity"],
            "usage_severity": report["usage_severity"],
            "packaging_damage": report.get("packaging_damage", 0),
            "missing_accessories": report["missing_accessories"],
            "ai_source": "gemini"
        }

    except Exception as e:
        logger.exception("Gemini grading failed, falling back to CLIP")
        return _grade_with_clip_fallback(image_bytes_list)


def _grade_with_clip_fallback(image_bytes_list: List[bytes]) -> Dict[str, Any]:
    """Fallback to the existing CLIP-based grading model."""
    try:
        from models.grading import grade_images
        result = grade_images(image_bytes_list)
        result["ai_source"] = "clip_fallback"
        return result
    except Exception as e:
        logger.error(f"CLIP fallback also failed: {e}")
        return {
            "condition_score": 70,
            "grade": "B",
            "confidence": 50,
            "defects_description": "Unable to assess — defaulting to Grade B",
            "detected_defects": [],
            "inspection_summary": "Fallback assessment",
            "buyer_trust_report": "Standard condition assumed",
            "ai_source": "fallback_default"
        }
