# =========================================================
# Listing Generation — Template-based (Mock Mistral)
# High-quality pre-written templates per category × grade
# =========================================================

import logging
import asyncio
import random

logger = logging.getLogger(__name__)

# ── Templates: category → grade → {title_template, description_template, tags} ──

LISTING_TEMPLATES = {
    "Electronics": {
        "A": {
            "title": "Certified Pre-Owned {name} — Like New | {warranty}% Warranty Remaining | Amazon Second Life Verified",
            "description": [
                "This {name} has been professionally inspected by Amazon's AI grading system and certified as Grade A — Like New condition. The product shows no visible wear, scratches, or defects and functions exactly as intended by the manufacturer.",
                "Originally priced at ₹{original_price}, this certified pre-owned unit comes with {warranty}% of its original warranty still intact, giving you complete peace of mind. Every Second Life product undergoes a multi-point AI inspection covering functionality, cosmetic condition, and completeness.",
                "By choosing this pre-owned product, you're not just saving money — you're contributing to Amazon's sustainability initiative. This purchase prevents one more electronic device from ending up in a landfill. Shipping is handled entirely by Amazon with the same reliability you trust.",
            ],
            "tags": ["certified-preowned", "like-new", "ai-graded", "warranty-active", "amazon-verified", "sustainable", "eco-friendly"],
        },
        "B": {
            "title": "{name} — Good Condition, Minor Cosmetic Wear | {warranty}% Warranty | Amazon Second Life",
            "description": [
                "This {name} has been inspected by Amazon's AI grading system and rated Grade B — Good condition with minor cosmetic wear. The product is fully functional with only light surface marks that do not affect performance.",
                "Priced at ₹{resale_price} (originally ₹{original_price}), this unit offers excellent value with {warranty}% warranty coverage remaining. Our AI detected: {defects}. All core features and specifications remain fully operational.",
                "Amazon Second Life products are verified for functionality before listing. Your purchase includes standard Amazon delivery and is backed by the remaining manufacturer warranty. A sustainable choice that gives great technology a second life.",
            ],
            "tags": ["good-condition", "minor-wear", "functional", "warranty-active", "value-deal", "sustainable"],
        },
    },
    "Baby Products": {
        "A": {
            "title": "Pre-Owned {name} — Excellent Condition | {warranty}% Warranty Left | Amazon Second Life Verified",
            "description": [
                "This {name} has been certified Grade A by Amazon's AI inspection — in excellent condition with no visible damage or wear. Perfect for parents looking for reliable baby products at a better price.",
                "With {warranty}% of the original warranty still valid, you get full manufacturer backing. Originally ₹{original_price}, now available through Amazon Second Life at ₹{resale_price}. Every baby product in our program undergoes extra safety verification.",
                "Choosing pre-owned baby products through Amazon's verified channel means you get quality assurance that private resale platforms cannot match. Secure packaging and Amazon delivery ensure your product arrives safely.",
            ],
            "tags": ["baby-safe", "excellent-condition", "warranty-active", "amazon-verified", "parent-approved", "sustainable"],
        },
        "B": {
            "title": "{name} — Good Condition | Minor Signs of Use | {warranty}% Warranty | Second Life",
            "description": [
                "This {name} is rated Grade B — good condition with minor signs of previous use. Fully functional and safe for daily use. AI inspection detected: {defects}.",
                "Available at ₹{resale_price} with {warranty}% warranty remaining (originally ₹{original_price}). All safety features have been verified operational. A smart choice for budget-conscious parents.",
                "Amazon Second Life ensures every baby product meets safety standards before relisting. Standard Amazon delivery and packaging applied.",
            ],
            "tags": ["good-condition", "baby-safe", "functional", "value-deal", "warranty-active", "sustainable"],
        },
    },
    "Apparel": {
        "A": {
            "title": "Like New {name} — Unused/Unworn | Amazon Second Life Verified",
            "description": [
                "This {name} has been AI-graded as Like New — showing no signs of wear. Likely returned due to size or color preference, this item is in pristine condition.",
                "Originally ₹{original_price}, now ₹{resale_price} through Amazon Second Life. The item has been inspected for stains, tears, and structural integrity — all clear.",
                "Give fashion a second chance. By purchasing pre-owned apparel through Amazon's verified channel, you're supporting sustainable fashion while getting premium products at better prices.",
            ],
            "tags": ["like-new", "unworn", "fashion", "sustainable-fashion", "amazon-verified", "size-return"],
        },
        "B": {
            "title": "{name} — Gently Used | Good Condition | Amazon Second Life",
            "description": [
                "This {name} shows minor signs of use but remains in good wearable condition. AI inspection detected: {defects}.",
                "Priced at ₹{resale_price} (was ₹{original_price}). All seams, zippers, and structural elements are intact and functional.",
                "A sustainable fashion choice through Amazon's trusted Second Life marketplace.",
            ],
            "tags": ["gently-used", "good-condition", "fashion", "value-deal", "sustainable"],
        },
    },
    "Fitness": {
        "A": {
            "title": "Pre-Owned {name} — Excellent Condition | Amazon Second Life",
            "description": [
                "This {name} has been AI-certified as Grade A — excellent condition with no damage. Perfect for fitness enthusiasts looking for quality equipment at a better price.",
                "Originally ₹{original_price}, now available at ₹{resale_price}. Fully functional with all original features intact.",
                "Amazon Second Life verified. Sustainable shopping that keeps fitness equipment out of landfills.",
            ],
            "tags": ["fitness", "excellent-condition", "amazon-verified", "sustainable", "value-deal"],
        },
        "B": {
            "title": "{name} — Good Condition, Light Use | Amazon Second Life",
            "description": [
                "This {name} is in good condition with minor cosmetic marks from previous use. AI detected: {defects}. Fully functional.",
                "₹{resale_price} (originally ₹{original_price}). All core functionality verified by Amazon's AI grading system.",
                "A sustainable choice for fitness gear. Amazon delivery and packaging included.",
            ],
            "tags": ["fitness", "good-condition", "functional", "sustainable", "value-deal"],
        },
    },
    "Home Goods": {
        "A": {
            "title": "Pre-Owned {name} — Like New Condition | Amazon Second Life Verified",
            "description": [
                "This {name} has been AI-graded as Like New. No visible damage, scratches, or wear detected. Fully functional and ready for use.",
                "Originally ₹{original_price}, available at ₹{resale_price} through Amazon Second Life. Quality home products deserve a second life.",
                "Amazon-verified condition with standard delivery. An eco-conscious choice for your home.",
            ],
            "tags": ["home", "like-new", "amazon-verified", "sustainable", "eco-friendly"],
        },
        "B": {
            "title": "{name} — Good Condition | Amazon Second Life",
            "description": [
                "This {name} shows minor signs of use. AI detected: {defects}. All core functionality is intact.",
                "₹{resale_price} (was ₹{original_price}). Verified by Amazon's AI grading for quality assurance.",
                "A sustainable home purchase through Amazon Second Life.",
            ],
            "tags": ["home", "good-condition", "functional", "value-deal", "sustainable"],
        },
    },
}

# Default template for unknown categories
DEFAULT_TEMPLATE = LISTING_TEMPLATES["Electronics"]


async def generate_listing(
    grade: str,
    product_name: str,
    product_category: str,
    defects_description: str,
    original_price: int,
    resale_price: int,
    warranty_pct: float = 50,
) -> dict:
    """
    Generate an Amazon-style product listing from templates.
    Adds a 2-second delay to simulate AI inference.

    Returns:
        dict with title, description, meta_tags, seo_score
    """
    # Simulate inference delay for demo realism
    await asyncio.sleep(2)

    # Get the right template
    category_templates = LISTING_TEMPLATES.get(product_category, DEFAULT_TEMPLATE)
    grade_key = grade if grade in ("A", "B") else "B"  # Grade C products don't get listed
    template = category_templates.get(grade_key, category_templates["B"])

    # Fill in dynamic values
    fill = {
        "name": product_name,
        "original_price": f"{original_price:,}",
        "resale_price": f"{resale_price:,}",
        "warranty": f"{warranty_pct:.0f}",
        "defects": defects_description or "minor cosmetic marks",
    }

    title = template["title"].format(**fill)
    description = "\n\n".join([p.format(**fill) for p in template["description"]])
    tags = template["tags"].copy()

    # Mock SEO score (82-96 range as per prompt)
    seo_score = random.randint(82, 96)

    return {
        "title": title,
        "description": description,
        "meta_tags": tags,
        "seo_score": seo_score,
    }
