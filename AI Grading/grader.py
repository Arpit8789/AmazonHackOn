import streamlit as st
import json
from PIL import Image
from io import BytesIO

from google import genai
from google.genai import types
from google.oauth2 import service_account


st.set_page_config(page_title="Product Condition Grading", layout="wide")

SERVICE_ACCOUNT_FILE = "service-account.json"
PROJECT_ID = "datatech-497104"
LOCATION = "us-central1"
GEMINI_MODEL = "gemini-2.5-flash"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    credentials=credentials
)


def uploaded_image_to_part(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=70)

    return types.Part.from_bytes(
        data=buffer.getvalue(),
        mime_type="image/jpeg"
    )


def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def fallback_report(message="Unable to parse AI response."):
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


def clean_json_response(text):
    try:
        text = text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        return json.loads(text)

    except Exception:
        st.error("Gemini did not return valid JSON. Showing raw response:")
        st.code(text)
        return fallback_report("Gemini returned incomplete or invalid JSON.")


def calculate_score(report):
    score = 100

    score -= safe_int(report.get("scratch_severity", 0)) * 3
    score -= safe_int(report.get("dent_severity", 0)) * 4
    score -= safe_int(report.get("crack_severity", 0)) * 8
    score -= safe_int(report.get("usage_severity", 0)) * 3
    score -= safe_int(report.get("packaging_damage", 0)) * 2

    if report.get("missing_accessories", False):
        score -= 15

    return max(0, min(100, round(score)))


def assign_grade(score):
    if score >= 90:
        return "A - Like New"
    elif score >= 75:
        return "B - Good Condition"
    elif score >= 60:
        return "C - Fair Condition"
    elif score >= 40:
        return "D - Poor Condition"
    else:
        return "Reject - Not Suitable for Resale"


def call_gemini(uploaded_images, description):
    prompt = f"""
You are an expert product condition inspector for resale.

Seller description:
"{description}"

Analyze the product images.

Return ONLY valid JSON.
Do not use markdown.
Do not write explanation outside JSON.
Do not add trailing commas.
Use only numbers for severity fields.
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

    image_parts = [uploaded_image_to_part(img) for img in uploaded_images[:3]]

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=2000,
                response_mime_type="application/json"
            )
        )

        raw_text = response.text.strip()

        st.subheader("Raw Gemini Response")
        st.code(raw_text)

        return clean_json_response(raw_text)

    except Exception as e:
        st.error("Gemini API call failed.")
        st.exception(e)
        return fallback_report("Gemini API call failed.")


st.title("Amazon Second Life Commerce - Product Condition Grading")

st.write(
    "Upload product images and add a short description. "
    "The AI will detect defects and assign a resale condition grade."
)

description = st.text_area(
    "Product Description",
    placeholder="Example: Used for 8 months. Minor scratches on the side. Charger and box included."
)

uploaded_images = st.file_uploader(
    "Upload product images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_images:
    st.subheader("Uploaded Images")
    cols = st.columns(min(4, len(uploaded_images)))

    for index, img in enumerate(uploaded_images):
        with cols[index % len(cols)]:
            st.image(img, caption=img.name, use_container_width=True)

if st.button("Grade Product"):
    if not uploaded_images:
        st.error("Please upload at least one product image.")
    elif not description.strip():
        st.error("Please enter a product description.")
    else:
        with st.spinner("Analyzing product condition using Gemini Vision..."):
            ai_report = call_gemini(uploaded_images, description)

            final_score = calculate_score(ai_report)
            final_grade = assign_grade(final_score)

            st.success("Product grading completed!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Final Condition Score", f"{final_score}/100")

            with col2:
                st.metric("Final Grade", final_grade)

            with col3:
                st.metric("AI Suggested Grade", ai_report.get("ai_recommended_grade", "N/A"))

            st.subheader("Detected Defects")

            defects = ai_report.get("detected_defects", [])

            if defects:
                for defect in defects:
                    st.write(
                        f"""
                        **Type:** {defect.get("type", "N/A")}  
                        **Severity:** {defect.get("severity", "N/A")}/10  
                        **Location:** {defect.get("location", "N/A")}  
                        **Confidence:** {defect.get("confidence", "N/A")}%
                        """
                    )
                    st.divider()
            else:
                st.info("No major visible defects detected.")

            st.subheader("Severity Breakdown")

            st.write({
                "Scratch Severity": ai_report.get("scratch_severity", 0),
                "Dent Severity": ai_report.get("dent_severity", 0),
                "Crack Severity": ai_report.get("crack_severity", 0),
                "Usage Severity": ai_report.get("usage_severity", 0),
                "Packaging Damage": ai_report.get("packaging_damage", 0),
                "Missing Accessories": ai_report.get("missing_accessories", False),
            })

            st.subheader("Inspection Summary")
            st.write(ai_report.get("inspection_summary", "No summary provided."))

            st.subheader("Buyer Trust Report")
            st.info(ai_report.get("buyer_trust_report", "No buyer trust report generated."))

            st.subheader("Parsed AI JSON")
            st.json(ai_report)