# =========================================================
# Pincode → Demand Level Mapping
# Used by grading + return routing to decide local vs warehouse
# =========================================================

DEMAND_MAP = {
    # HIGH demand cities
    "110001": {"city": "Delhi",     "demand": "HIGH",   "score": 0.9},
    "110020": {"city": "Delhi",     "demand": "HIGH",   "score": 0.9},
    "400001": {"city": "Mumbai",    "demand": "HIGH",   "score": 0.88},
    "400050": {"city": "Mumbai",    "demand": "HIGH",   "score": 0.88},
    "560001": {"city": "Bangalore", "demand": "HIGH",   "score": 0.85},
    "560100": {"city": "Bangalore", "demand": "HIGH",   "score": 0.85},

    # MEDIUM demand cities
    "302001": {"city": "Jaipur",    "demand": "MEDIUM", "score": 0.55},
    "302020": {"city": "Jaipur",    "demand": "MEDIUM", "score": 0.55},
    "500001": {"city": "Hyderabad", "demand": "MEDIUM", "score": 0.6},
    "411001": {"city": "Pune",      "demand": "MEDIUM", "score": 0.58},
    "600001": {"city": "Chennai",   "demand": "MEDIUM", "score": 0.62},

    # LOW demand cities
    "800001": {"city": "Patna",     "demand": "LOW",    "score": 0.25},
    "226001": {"city": "Lucknow",   "demand": "LOW",    "score": 0.3},
    "452001": {"city": "Indore",    "demand": "LOW",    "score": 0.28},
}

# Default for unknown pincodes
DEFAULT_DEMAND = {"city": "Unknown", "demand": "MEDIUM", "score": 0.5}


def get_demand(pincode: str) -> dict:
    """Look up regional demand for a pincode."""
    return DEMAND_MAP.get(pincode, DEFAULT_DEMAND)
