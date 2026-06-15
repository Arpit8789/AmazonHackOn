export const fallbackData = {
  products: [
    {
      product_id: "P001",
      name: "Noise ColorFit Pro 4 Smartwatch",
      category: "Electronics",
      original_price: 3499,
      image_url: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80",
      order_id: "403-1234567-8901234",
      purchase_date: "2025-01-10",
      resale_eligible: true
    },
    {
      product_id: "P003",
      name: "Philips Avent Baby Monitor SCD841",
      category: "Baby Products",
      original_price: 4999,
      image_url: "https://images.unsplash.com/photo-1590249476095-eef4f7d3b42f?w=400&q=80",
      order_id: "403-5551234-3334567",
      purchase_date: "2026-12-15",
      resale_eligible: true
    }
  ],
  returnInitiate: {
    order_id: "403-1234567-8901234",
    next_step: "photo_upload",
    photo_count_required: 3,
    angle_guide: ["Front view", "Back view", "Defect area (if any)"],
    demand_info: { city: "Delhi", demand: "HIGH", score: 0.9 }
  },
  grade: {
    grade: "A",
    confidence: 94.2,
    confidence_gap: 18.5,
    needs_human_review: false,
    defects_description: "No visible defects detected. Product appears to be in excellent, like-new condition.",
    routing_decision: "✓ Routed to local Delhi fulfillment node",
    recommended_action: "local_relist_full",
    demand_level: "HIGH",
    demand_region: "Delhi"
  },
  price: {
    price_low: 2800,
    price_high: 3400,
    predicted_value: 3100,
    shap_explanation: [
      { factor: "Warranty remaining: 58%", impact_inr: "+₹1,200", direction: "positive" },
      { factor: "High regional demand", impact_inr: "+₹300", direction: "positive" }
    ],
    breakdown: {
      resale_value: "₹2,800 — ₹3,400",
      packaging_cost: 40,
      reprocessing_charge: 30,
      amazon_platform_fee_7pct: 238,
      delivery_charge: 80,
      delivery_zone: "Nearby cities"
    },
    seller_receives: 2770
  },
  resaleSubmit: {
    listing_id: "SL-A8F9B2",
    status: "live",
    listing_url: "/second-life/listing/SL-A8F9B2",
    estimated_sale_days: 4,
    message: "Your product is now live on Amazon Second Life!"
  },
  sellerAutolist: {
    grade: { grade: "B", defects_description: "Minor cosmetic wear" },
    price: { price_high: 1800 },
    listing: {
      title: "Anker 7-in-1 USB-C Hub — Good Condition | Amazon Second Life",
      description: "This item has been AI-graded as Grade B...",
      meta_tags: ["good-condition", "amazon-verified"],
      seo_score: 88
    },
    processing_time_seconds: 1.4,
    time_saved_minutes: 25
  },
  reviewQA: {
    answer: "Based on customer reviews, the battery easily lasts 5-6 days with normal use. It charges fully in about 1.5 to 2 hours.",
    language_detected: "en",
    confidence: 88.5,
    source_reviews: [
      { user: "Rahul K.", rating: 5, text: "Battery easily lasts 5-6 days with normal use." }
    ]
  }
};
