# Amazon Second Life Commerce – AI-Powered Resale Pricing & Product Grading

## Overview

Amazon Second Life Commerce is an AI-powered resale platform that helps users resell previously purchased products by automatically assessing product condition, verifying warranty eligibility, predicting fair resale value, and generating transparent explanations for the predicted price.

The system combines:

* AI-based product inspection using Gemini Vision
* Automated defect detection
* Condition grading
* Warranty validation
* Machine Learning-based resale price prediction
* Explainable AI (SHAP)
* Business-friendly explanations

The objective is to create trust in second-life commerce while reducing waste and enabling sustainable resale.

---

## Problem Statement

Millions of products are returned, underutilized, or discarded despite being perfectly usable.

Current resale systems suffer from:

* Manual inspection overhead
* Inconsistent pricing
* Lack of trust
* Poor transparency
* High operational costs

Our solution automates product inspection and resale valuation using AI.

---

## Key Features

### AI Product Inspection

The system analyzes uploaded product images using Gemini Vision and automatically identifies:

* Scratches
* Dents
* Cracks
* Signs of wear and tear
* Missing accessories
* Packaging damage

---

### Automated Condition Grading

Products receive:

* Condition Score (0–100)
* Condition Grade

Grades:

| Grade  | Meaning                 |
| ------ | ----------------------- |
| A      | Like New                |
| B      | Good Condition          |
| C      | Fair Condition          |
| D      | Poor Condition          |
| Reject | Not Suitable for Resale |

---

### Warranty Eligibility Engine

To improve buyer trust, products are eligible for resale only if:

warranty_left_days >= max(60, 25% of initial_warranty_days)

Example:

* Initial Warranty = 365 days
* Minimum Required = 91 days

Products failing this criterion are automatically rejected.

---

### Resale Price Prediction

The system predicts a fair resale price using a CatBoost Regressor trained on a dataset of approximately 10,000 product records.

Input Features:

* Product category
* Brand
* Purchase price
* Current market price
* Product age
* Warranty remaining
* Condition score
* Defect severity
* Missing accessories

Output:

* Predicted resale price
* Confidence score

---

### Explainable AI (XAI)

SHAP is used to explain model predictions.

Example:

Predicted Price: ₹44,399

Positive Contributors:

* Excellent condition
* Premium brand
* Warranty remaining

Negative Contributors:

* Product age
* Visible scratches
* Limited warranty remaining

---

## Architecture

User Uploads Images
↓
Gemini Vision Inspection
↓
Defect Detection
↓
Condition Score Calculation
↓
Warranty Eligibility Engine
↓
Feature Engineering
↓
CatBoost Price Prediction
↓
SHAP Explainability
↓
Business Explanation Layer
↓
JSON API Response

---

## Technology Stack

### Backend

* FastAPI
* Python

### AI & ML

* Gemini 2.5 Flash
* CatBoost
* SHAP
* Scikit-Learn

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Deployment

* Uvicorn
* Google Vertex AI

---

## Project Structure

```text
project/
│
├── resale_api.py
├── train_resale_price_model.py
├── requirements.txt
├── README.md
│
├── artifacts/
│   ├── resale_price_inference_engine.pkl
│   ├── best_model_metrics.json
│   ├── training_report.txt
│   └── ...
│
└── sample_images/
```

## Installation

### Clone Repository

```bash
git clone <repository_url>
cd project
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Google Vertex AI Setup

Create a Google Cloud service account.

Download the service account key.

Place it in the project root:

```text
service-account.json
```

Update configuration inside:

```python
SERVICE_ACCOUNT_FILE = "service-account.json"
PROJECT_ID = "<your-project-id>"
LOCATION = "us-central1"
```

---

## Training the Model

```bash
python train_resale_price_model.py
```

Artifacts generated:

```text
artifacts/
```

including:

* Trained model
* Metrics
* Reports
* SHAP visualizations

---

## Running the API

```bash
uvicorn resale_api:app --reload --host 0.0.0.0 --port 8000
```

Health Check:

```text
GET /health
```

---

## Main API Endpoint

### POST /predict-resale

Input:

* Product Images
* Product Description
* Product Category
* Brand
* Purchase Price
* Current Market Price
* Purchase Date
* Initial Warranty Days

Output:

```json
{
  "eligible_for_resale": true,
  "recommended_listing_price": 44399,
  "prediction": {
    "confidence_score": 81.49,
    "top_positive_factors": [
      "Excellent condition",
      "Premium brand"
    ],
    "top_negative_factors": [
      "Product age"
    ]
  }
}
```

---

## Model Performance

Best Model:

CatBoost Regressor

Metrics:

* MAE: 1559
* RMSE: 3218
* R²: 0.9887
* MAPE: 11.94%

Cross Validation:

* Mean R²: 0.9878

---

## Business Impact

### For Customers

* Fair pricing
* Transparent valuation
* Increased trust

### For Sellers

* Instant resale recommendations
* Reduced manual effort
* Faster listing process

### For Amazon

* Reduced waste
* Sustainable commerce
* Increased resale marketplace participation

---

## Future Enhancements

* Seller fraud detection
* Authenticity verification
* Dynamic market price scraping
* Refurbishment recommendation engine
* Carbon footprint savings estimation
* Multi-modal LLM reasoning
* Real-time pricing updates

---

## Team

Amazon HackOn 5.0 Submission

Second Life Commerce: AI-Powered Returns & Sustainable Resale
