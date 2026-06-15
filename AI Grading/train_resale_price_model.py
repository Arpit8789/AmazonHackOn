#!/usr/bin/env python3
"""
train_resale_price_model.py

Production-grade resale price prediction training pipeline for an Amazon-style
Second Life Commerce platform.

Author: Generated for Amazon HackOn-style resale pricing system

How to run:
    python train_resale_price_model.py --data_path resale_dataset.csv

Optional:
    python train_resale_price_model.py --data_path resale_dataset.csv --output_dir artifacts --fast_mode

Expected target column:
    resale_price
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import pickle
import warnings
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# Force a non-GUI backend for Windows/server environments.
# This prevents Tkinter errors such as:
# RuntimeError: main thread is not in main loop
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.experimental import enable_hist_gradient_boosting  # noqa: F401
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.feature_selection import mutual_info_regression
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (
    KFold,
    RandomizedSearchCV,
    cross_validate,
    train_test_split,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

try:
    from lightgbm import LGBMRegressor
    LIGHTGBM_AVAILABLE = True
except Exception:
    LIGHTGBM_AVAILABLE = False

try:
    from catboost import CatBoostRegressor
    CATBOOST_AVAILABLE = True
except Exception:
    CATBOOST_AVAILABLE = False

RANDOM_STATE = 42
TARGET = "resale_price"

RAW_COLUMNS = [
    "product_category",
    "product_name",
    "brand",
    "current_market_price",
    "purchase_price",
    "purchase_age_days",
    "initial_warranty_days",
    "warranty_left_days",
    "condition_score",
    "condition_grade",
    "scratch_severity",
    "dent_severity",
    "crack_severity",
    "usage_severity",
    "missing_accessories",
    "seller_description",
    "resale_price",
]

BASE_EXCLUDED_FEATURES = [
    TARGET,
    "seller_description",
    "product_name",
]

SUPPORTED_CATEGORIES = {
    "Mobile Phones",
    "Laptops",
    "Tablets",
    "Smart Watches",
    "Headphones",
    "Refrigerators",
    "Washing Machines",
    "Microwaves",
    "Televisions",
    "Furniture",
}

PREMIUM_BRANDS = {
    "Apple", "Samsung", "Sony", "Dell", "HP", "Lenovo", "LG", "Bosch",
    "Whirlpool", "OnePlus", "Google", "Microsoft", "Asus", "JBL", "Bose",
    "Panasonic", "Haier", "Xiaomi", "Nike", "Ikea"
}

ELECTRONICS_CATEGORIES = {
    "Mobile Phones", "Laptops", "Tablets", "Smart Watches", "Headphones",
    "Microwaves", "Televisions"
}

FURNITURE_CATEGORIES = {"Furniture"}


@dataclass
class ModelMetrics:
    model_name: str
    mae: float
    rmse: float
    mse: float
    r2: float
    mape: float
    cv_mae_mean: Optional[float] = None
    cv_mae_std: Optional[float] = None
    cv_rmse_mean: Optional[float] = None
    cv_rmse_std: Optional[float] = None
    cv_r2_mean: Optional[float] = None
    cv_r2_std: Optional[float] = None


def setup_logging(output_dir: Path) -> logging.Logger:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = output_dir / "training.log"

    logger = logging.getLogger("resale_price_training")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def safe_divide(a: pd.Series, b: pd.Series, default: float = 0.0) -> pd.Series:
    result = a / b.replace(0, np.nan)
    return result.replace([np.inf, -np.inf], np.nan).fillna(default)


def mape_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    denom = np.where(np.abs(y_true) < 1e-8, 1.0, np.abs(y_true))
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100)


def rmse_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(math.sqrt(mean_squared_error(y_true, y_pred)))


def save_json(obj: Any, path: Path) -> None:
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


def save_pickle(obj: Any, path: Path) -> None:
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_csv(data_path: Path, logger: logging.Logger) -> pd.DataFrame:
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    df = pd.read_csv(data_path)
    df.columns = [c.strip() for c in df.columns]

    logger.info("Loaded dataset from %s", data_path)
    logger.info("Dataset shape: %s", df.shape)

    missing_cols = [c for c in RAW_COLUMNS if c not in df.columns]
    if missing_cols:
        logger.warning("Missing expected columns: %s", missing_cols)

    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in dataset.")

    return df


def generate_eda_report(df: pd.DataFrame, output_dir: Path, logger: logging.Logger) -> None:
    eda_dir = output_dir / "eda"
    eda_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting EDA...")

    report_lines = []
    report_lines.append("# EDA Report\n")
    report_lines.append(f"Generated at: {datetime.now()}\n")
    report_lines.append(f"Shape: {df.shape}\n\n")

    report_lines.append("## Columns\n")
    report_lines.append(str(df.dtypes))
    report_lines.append("\n\n## Missing Values\n")
    report_lines.append(str(df.isna().sum().sort_values(ascending=False)))
    report_lines.append("\n\n## Duplicate Rows\n")
    report_lines.append(str(df.duplicated().sum()))
    report_lines.append("\n\n## Statistical Summary\n")
    report_lines.append(str(df.describe(include="all").T))

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    if numeric_cols:
        corr = df[numeric_cols].corr(numeric_only=True)
        corr.to_csv(eda_dir / "correlation_matrix.csv")

        plt.figure(figsize=(14, 10))
        sns.heatmap(corr, cmap="coolwarm", center=0, linewidths=0.3)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(eda_dir / "correlation_heatmap.png", dpi=160)
        plt.close()

        for col in numeric_cols:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f"Distribution of {col}")
            plt.tight_layout()
            plt.savefig(eda_dir / f"hist_{col}.png", dpi=140)
            plt.close()

            plt.figure(figsize=(8, 4))
            sns.boxplot(x=df[col].dropna())
            plt.title(f"Boxplot of {col}")
            plt.tight_layout()
            plt.savefig(eda_dir / f"boxplot_{col}.png", dpi=140)
            plt.close()

        relationship_cols = [
            c for c in [
                "current_market_price",
                "purchase_price",
                "purchase_age_days",
                "warranty_left_days",
                "condition_score",
                "scratch_severity",
                "dent_severity",
                "crack_severity",
                "usage_severity",
                TARGET,
            ] if c in df.columns
        ]
        if len(relationship_cols) >= 3:
            sample_df = df[relationship_cols].dropna()
            if len(sample_df) > 1500:
                sample_df = sample_df.sample(1500, random_state=RANDOM_STATE)
            sns.pairplot(sample_df)
            plt.savefig(eda_dir / "pairplot_numeric_relationships.png", dpi=120)
            plt.close()

    for col in categorical_cols:
        counts = df[col].value_counts(dropna=False).head(30)
        counts.to_csv(eda_dir / f"distribution_{col}.csv")

        plt.figure(figsize=(10, 5))
        counts.plot(kind="bar")
        plt.title(f"Top Distribution: {col}")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(eda_dir / f"bar_{col}.png", dpi=140)
        plt.close()

    key_relationships = [
        ("condition_score", TARGET),
        ("purchase_age_days", TARGET),
        ("warranty_left_days", TARGET),
        ("current_market_price", TARGET),
        ("crack_severity", TARGET),
    ]
    for x, y in key_relationships:
        if x in df.columns and y in df.columns:
            plt.figure(figsize=(8, 5))
            sns.scatterplot(data=df.sample(min(len(df), 2500), random_state=RANDOM_STATE), x=x, y=y, alpha=0.5)
            sns.regplot(data=df.sample(min(len(df), 2500), random_state=RANDOM_STATE), x=x, y=y, scatter=False)
            plt.title(f"{x} vs {y}")
            plt.tight_layout()
            plt.savefig(eda_dir / f"relationship_{x}_vs_{y}.png", dpi=140)
            plt.close()

    (eda_dir / "eda_report.txt").write_text("\n".join(report_lines), encoding="utf-8")
    logger.info("EDA completed. Reports saved to %s", eda_dir)


def clean_and_validate(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    logger.info("Starting validation and cleaning...")
    original_rows = len(df)
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})

    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()
    logger.info("Removed duplicate rows: %d", duplicate_count)

    numeric_columns = [
        "current_market_price", "purchase_price", "purchase_age_days",
        "initial_warranty_days", "warranty_left_days", "condition_score",
        "scratch_severity", "dent_severity", "crack_severity", "usage_severity",
        TARGET,
    ]

    for col in numeric_columns:
        if col in df.columns:
            before_null = df[col].isna().sum()
            df[col] = pd.to_numeric(df[col], errors="coerce")
            after_null = df[col].isna().sum()
            if after_null > before_null:
                logger.info("Converted invalid numeric values to NaN in %s: %d", col, after_null - before_null)

    before = len(df)
    required_for_training = [
        "current_market_price", "purchase_price", "purchase_age_days",
        "initial_warranty_days", "warranty_left_days", "condition_score",
        "scratch_severity", "dent_severity", "crack_severity", "usage_severity",
        TARGET,
    ]
    existing_required = [c for c in required_for_training if c in df.columns]
    df = df.dropna(subset=existing_required)
    logger.info("Removed rows with missing critical numeric fields: %d", before - len(df))

    before = len(df)
    price_cols = ["current_market_price", "purchase_price", TARGET]
    for c in price_cols:
        if c in df.columns:
            df = df[df[c] > 0]
    logger.info("Removed invalid non-positive price rows: %d", before - len(df))

    before = len(df)
    non_negative_cols = [
        "purchase_age_days", "initial_warranty_days", "warranty_left_days",
        "scratch_severity", "dent_severity", "crack_severity", "usage_severity",
    ]
    for c in non_negative_cols:
        if c in df.columns:
            df = df[df[c] >= 0]
    logger.info("Removed rows with negative numeric values: %d", before - len(df))

    before = len(df)
    if "condition_score" in df.columns:
        df = df[(df["condition_score"] >= 0) & (df["condition_score"] <= 100)]
    logger.info("Removed invalid condition score rows: %d", before - len(df))

    before = len(df)
    severity_cols = ["scratch_severity", "dent_severity", "crack_severity", "usage_severity"]
    for c in severity_cols:
        if c in df.columns:
            df = df[(df[c] >= 0) & (df[c] <= 10)]
    logger.info("Removed invalid defect severity rows: %d", before - len(df))

    before = len(df)
    if "warranty_left_days" in df.columns and "initial_warranty_days" in df.columns:
        df = df[df["warranty_left_days"] <= df["initial_warranty_days"]]
    logger.info("Removed impossible warranty rows: %d", before - len(df))

    before = len(df)
    if "current_market_price" in df.columns and TARGET in df.columns:
        df = df[df[TARGET] <= df["current_market_price"] * 1.25]
    logger.info("Removed extreme resale price outliers above 125%% of market price: %d", before - len(df))

    for col in ["product_category", "brand", "condition_grade", "missing_accessories"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "missing_accessories" in df.columns:
        df["missing_accessories"] = df["missing_accessories"].astype(str).str.lower().replace({
            "yes": "Yes", "true": "Yes", "1": "Yes",
            "no": "No", "false": "No", "0": "No",
            "unknown": "Unknown",
        })

    logger.info("Cleaning completed. Rows before: %d, rows after: %d", original_rows, len(df))
    return df.reset_index(drop=True)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Stateless feature engineering transformer.

    This class is intentionally sklearn-compatible so the same feature creation
    logic is used during both training and inference.
    """

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "FeatureEngineer":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        required_numeric = [
            "current_market_price", "purchase_price", "purchase_age_days",
            "initial_warranty_days", "warranty_left_days", "condition_score",
            "scratch_severity", "dent_severity", "crack_severity", "usage_severity",
        ]
        for c in required_numeric:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        for c in ["product_category", "brand", "condition_grade", "missing_accessories"]:
            if c not in df.columns:
                df[c] = "Unknown"
            df[c] = df[c].fillna("Unknown").astype(str)

        df["warranty_ratio"] = safe_divide(df["warranty_left_days"], df["initial_warranty_days"])
        df["age_years"] = df["purchase_age_days"] / 365.0

        # Product of defect severities captures compounding damage risk.
        df["defect_score"] = (
            df["scratch_severity"] *
            df["dent_severity"] *
            df["crack_severity"] *
            df["usage_severity"]
        )

        # Weighted sum is more stable than product and assigns cracks the highest penalty.
        df["weighted_defect_score"] = (
            1.0 * df["scratch_severity"] +
            2.0 * df["dent_severity"] +
            5.0 * df["crack_severity"] +
            2.0 * df["usage_severity"]
        )

        df["condition_age_interaction"] = df["condition_score"] * df["warranty_ratio"]
        df["age_warranty_interaction"] = df["age_years"] * df["warranty_ratio"]
        df["price_retention_ratio"] = safe_divide(df["current_market_price"], df["purchase_price"], default=1.0)
        df["total_damage_score"] = (
            df["scratch_severity"] +
            df["dent_severity"] +
            df["crack_severity"] +
            df["usage_severity"]
        )

        df["premium_brand_flag"] = df["brand"].isin(PREMIUM_BRANDS).astype(int)
        df["high_value_product_flag"] = (df["current_market_price"] >= df["current_market_price"].quantile(0.75)).astype(int)
        df["electronics_flag"] = df["product_category"].isin(ELECTRONICS_CATEGORIES).astype(int)
        df["furniture_flag"] = df["product_category"].isin(FURNITURE_CATEGORIES).astype(int)
        df["expired_warranty_flag"] = (df["warranty_left_days"] <= 0).astype(int)
        df["long_warranty_flag"] = (df["warranty_ratio"] >= 0.5).astype(int)
        df["excellent_condition_flag"] = (df["condition_score"] >= 85).astype(int)
        df["heavily_damaged_flag"] = (df["weighted_defect_score"] >= 35).astype(int)

        df["market_price_log"] = np.log1p(df["current_market_price"])
        df["purchase_price_log"] = np.log1p(df["purchase_price"])
        df["age_log"] = np.log1p(df["purchase_age_days"])
        df["warranty_left_log"] = np.log1p(df["warranty_left_days"])
        df["condition_squared"] = df["condition_score"] ** 2
        df["damage_condition_ratio"] = safe_divide(df["total_damage_score"], df["condition_score"] + 1)

        df["is_supported_hackon_category"] = df["product_category"].isin(SUPPORTED_CATEGORIES).astype(int)
        df["missing_accessories_flag"] = df["missing_accessories"].astype(str).str.lower().isin(["yes", "true", "1"]).astype(int)

        return df


def get_model_feature_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c not in BASE_EXCLUDED_FEATURES]


def analyze_feature_selection(
    engineered_df: pd.DataFrame,
    target: pd.Series,
    output_dir: Path,
    logger: logging.Logger,
) -> Dict[str, Any]:
    fs_dir = output_dir / "feature_selection"
    fs_dir.mkdir(parents=True, exist_ok=True)

    feature_cols = get_model_feature_columns(engineered_df)
    X = engineered_df[feature_cols].copy()

    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    correlations = {}
    for col in numeric_cols:
        try:
            correlations[col] = float(np.corrcoef(X[col].fillna(0), target)[0, 1])
        except Exception:
            correlations[col] = None

    corr_df = (
        pd.DataFrame({"feature": list(correlations.keys()), "correlation_with_target": list(correlations.values())})
        .sort_values("correlation_with_target", key=lambda s: s.abs(), ascending=False)
    )
    corr_df.to_csv(fs_dir / "correlation_analysis.csv", index=False)

    mi_scores = []
    if numeric_cols:
        X_num = X[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
        mi = mutual_info_regression(X_num, target, random_state=RANDOM_STATE)
        mi_scores = [{"feature": f, "mutual_information": float(v)} for f, v in zip(numeric_cols, mi)]
        pd.DataFrame(mi_scores).sort_values("mutual_information", ascending=False).to_csv(
            fs_dir / "mutual_information.csv", index=False
        )

    leakage_blocklist = [TARGET, "seller_description", "product_name"]
    selected_features = [c for c in feature_cols if c not in leakage_blocklist]

    reasoning = {
        "excluded_features": {
            TARGET: "Target variable. Including it would cause target leakage.",
            "seller_description": "Excluded from baseline to avoid noisy free-text and possible leakage.",
            "product_name": "Excluded from baseline to avoid high-cardinality memorization.",
        },
        "selected_feature_count": len(selected_features),
        "selected_features": selected_features,
        "numeric_features": numeric_cols,
        "categorical_features": categorical_cols,
        "feature_selection_logic": (
            "All validated structured features and engineered features are retained for tree/boosting models. "
            "Correlation and mutual information reports are exported for analysis. "
            "Leakage-prone fields are excluded."
        ),
    }
    save_json(reasoning, fs_dir / "feature_selection_reasoning.json")
    logger.info("Feature selection analysis completed.")
    return reasoning


def build_preprocessor(feature_df: pd.DataFrame, selected_features: List[str]) -> ColumnTransformer:
    X = feature_df[selected_features]
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def build_models(fast_mode: bool = False) -> Dict[str, Tuple[Any, Dict[str, List[Any]]]]:
    models = {
        "Linear Regression": (
            LinearRegression(),
            {},
        ),
        "Ridge Regression": (
            Ridge(random_state=RANDOM_STATE),
            {"model__alpha": [0.1, 1.0, 5.0, 10.0, 50.0]},
        ),
        "Random Forest Regressor": (
            RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            {
                "model__n_estimators": [100, 200] if fast_mode else [150, 250, 400],
                "model__max_depth": [None, 8, 12, 18],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
        ),
        "Extra Trees Regressor": (
            ExtraTreesRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            {
                "model__n_estimators": [100, 200] if fast_mode else [150, 250, 400],
                "model__max_depth": [None, 8, 12, 18],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            },
        ),
        "HistGradientBoosting Regressor": (
            HistGradientBoostingRegressor(random_state=RANDOM_STATE),
            {
                "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
                "model__max_iter": [100, 200] if fast_mode else [150, 250, 400],
                "model__max_leaf_nodes": [15, 31, 63],
                "model__l2_regularization": [0.0, 0.1, 1.0],
            },
        ),
    }

    if XGBOOST_AVAILABLE:
        models["XGBoost Regressor"] = (
            XGBRegressor(
                objective="reg:squarederror",
                random_state=RANDOM_STATE,
                n_jobs=-1,
                tree_method="hist",
            ),
            {
                "model__n_estimators": [100, 200] if fast_mode else [150, 300, 500],
                "model__max_depth": [3, 5, 7, 9],
                "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
                "model__subsample": [0.8, 0.9, 1.0],
                "model__colsample_bytree": [0.8, 0.9, 1.0],
            },
        )

    if LIGHTGBM_AVAILABLE:
        models["LightGBM Regressor"] = (
            LGBMRegressor(random_state=RANDOM_STATE, n_jobs=-1, verbose=-1),
            {
                "model__n_estimators": [100, 200] if fast_mode else [150, 300, 500],
                "model__num_leaves": [15, 31, 63],
                "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
                "model__subsample": [0.8, 0.9, 1.0],
                "model__colsample_bytree": [0.8, 0.9, 1.0],
            },
        )

    if CATBOOST_AVAILABLE:
        models["CatBoost Regressor"] = (
            CatBoostRegressor(
                random_seed=RANDOM_STATE,
                verbose=False,
                loss_function="RMSE",
            ),
            {
                "model__iterations": [100, 200] if fast_mode else [200, 400, 600],
                "model__depth": [4, 6, 8],
                "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
                "model__l2_leaf_reg": [1, 3, 5, 7],
            },
        )

    return models


def evaluate_predictions(model_name: str, y_true: np.ndarray, y_pred: np.ndarray) -> ModelMetrics:
    mse = float(mean_squared_error(y_true, y_pred))
    return ModelMetrics(
        model_name=model_name,
        mae=float(mean_absolute_error(y_true, y_pred)),
        rmse=float(math.sqrt(mse)),
        mse=mse,
        r2=float(r2_score(y_true, y_pred)),
        mape=mape_score(y_true, y_pred),
    )


def train_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
    output_dir: Path,
    logger: logging.Logger,
    fast_mode: bool = False,
) -> Tuple[str, Pipeline, pd.DataFrame, Dict[str, Any]]:
    logger.info("Starting model training...")

    model_dir = output_dir / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    models = build_models(fast_mode=fast_mode)
    results = []
    trained_models: Dict[str, Pipeline] = {}
    search_details: Dict[str, Any] = {}

    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    for model_name, (model, param_dist) in models.items():
        logger.info("Training model: %s", model_name)

        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ])

        if param_dist:
            n_iter = 5 if fast_mode else min(15, max(5, sum(len(v) for v in param_dist.values())))
            search = RandomizedSearchCV(
                estimator=pipeline,
                param_distributions=param_dist,
                n_iter=n_iter,
                scoring="neg_mean_absolute_error",
                cv=3 if fast_mode else 5,
                random_state=RANDOM_STATE,
                n_jobs=1,
                verbose=0,
                error_score="raise",
            )
            search.fit(X_train, y_train)
            best_pipeline = search.best_estimator_
            search_details[model_name] = {
                "best_params": search.best_params_,
                "best_cv_neg_mae": float(search.best_score_),
            }
        else:
            best_pipeline = pipeline.fit(X_train, y_train)
            search_details[model_name] = {"best_params": {}, "best_cv_neg_mae": None}

        y_pred = best_pipeline.predict(X_test)
        metrics = evaluate_predictions(model_name, y_test.values, y_pred)

        scoring = {
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
            "r2": "r2",
        }
        cv_results = cross_validate(
            best_pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=1,
            error_score="raise",
        )

        metrics.cv_mae_mean = float(-cv_results["test_mae"].mean())
        metrics.cv_mae_std = float(cv_results["test_mae"].std())
        metrics.cv_rmse_mean = float(-cv_results["test_rmse"].mean())
        metrics.cv_rmse_std = float(cv_results["test_rmse"].std())
        metrics.cv_r2_mean = float(cv_results["test_r2"].mean())
        metrics.cv_r2_std = float(cv_results["test_r2"].std())

        results.append(asdict(metrics))
        trained_models[model_name] = best_pipeline

        save_pickle(best_pipeline, model_dir / f"{model_name.replace(' ', '_').lower()}.pkl")
        logger.info(
            "%s | MAE=%.3f RMSE=%.3f R2=%.4f MAPE=%.2f%%",
            model_name, metrics.mae, metrics.rmse, metrics.r2, metrics.mape
        )

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(
        by=["mae", "r2", "rmse"],
        ascending=[True, False, True],
    )
    results_df.to_csv(output_dir / "model_comparison_table.csv", index=False)

    best_name = str(results_df.iloc[0]["model_name"])
    best_model = trained_models[best_name]

    logger.info("Best model selected: %s", best_name)
    return best_name, best_model, results_df, search_details


def generate_evaluation_plots(
    best_model: Pipeline,
    model_name: str,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    comparison_df: pd.DataFrame,
    output_dir: Path,
    logger: logging.Logger,
) -> None:
    eval_dir = output_dir / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    y_pred = best_model.predict(X_test)
    residuals = y_test.values - y_pred

    plt.figure(figsize=(7, 7))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
    min_v, max_v = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
    plt.plot([min_v, max_v], [min_v, max_v], "--")
    plt.xlabel("Actual Resale Price")
    plt.ylabel("Predicted Resale Price")
    plt.title(f"Actual vs Predicted - {model_name}")
    plt.tight_layout()
    plt.savefig(eval_dir / "actual_vs_predicted.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=y_pred, y=residuals, alpha=0.6)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Predicted Resale Price")
    plt.ylabel("Residual")
    plt.title("Residual Plot")
    plt.tight_layout()
    plt.savefig(eval_dir / "residual_plot.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(residuals, kde=True)
    plt.xlabel("Prediction Error")
    plt.title("Error Distribution")
    plt.tight_layout()
    plt.savefig(eval_dir / "error_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.barplot(data=comparison_df, x="model_name", y="mae")
    plt.xticks(rotation=45, ha="right")
    plt.title("Model Comparison by MAE")
    plt.tight_layout()
    plt.savefig(eval_dir / "model_comparison_mae.png", dpi=160)
    plt.close()

    logger.info("Evaluation plots saved.")


def get_transformed_feature_names(pipeline: Pipeline) -> List[str]:
    preprocessor = pipeline.named_steps["preprocessor"]
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        return [f"feature_{i}" for i in range(preprocessor.transformers_.shape[0])]


def generate_feature_importance_report(
    best_model: Pipeline,
    output_dir: Path,
    logger: logging.Logger,
) -> pd.DataFrame:
    report_dir = output_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    model = best_model.named_steps["model"]
    feature_names = get_transformed_feature_names(best_model)

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(np.ravel(model.coef_))
    else:
        importances = np.zeros(len(feature_names))

    length = min(len(feature_names), len(importances))
    df = pd.DataFrame({
        "feature": feature_names[:length],
        "importance": importances[:length],
    }).sort_values("importance", ascending=False)

    df.to_csv(report_dir / "feature_importance_report.csv", index=False)

    if not df.empty:
        plt.figure(figsize=(10, 8))
        sns.barplot(data=df.head(30), y="feature", x="importance")
        plt.title("Top Feature Importances")
        plt.tight_layout()
        plt.savefig(report_dir / "feature_importance_top30.png", dpi=160)
        plt.close()

    logger.info("Feature importance report saved.")
    return df


def generate_shap_reports(
    best_model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    output_dir: Path,
    logger: logging.Logger,
) -> Optional[pd.DataFrame]:
    shap_dir = output_dir / "shap"
    shap_dir.mkdir(parents=True, exist_ok=True)

    if not SHAP_AVAILABLE:
        logger.warning("SHAP is not installed. Skipping SHAP reports.")
        (shap_dir / "shap_unavailable.txt").write_text(
            "SHAP package not installed. Install with: pip install shap\n",
            encoding="utf-8"
        )
        return None

    try:
        preprocessor = best_model.named_steps["preprocessor"]
        model = best_model.named_steps["model"]

        X_sample = X_test.sample(min(len(X_test), 500), random_state=RANDOM_STATE)
        X_transformed = preprocessor.transform(X_sample)
        feature_names = get_transformed_feature_names(best_model)

        # TreeExplainer is fastest for tree models. Fallback to generic Explainer.
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_transformed)
        except Exception:
            background = preprocessor.transform(X_train.sample(min(len(X_train), 200), random_state=RANDOM_STATE))
            explainer = shap.Explainer(model.predict, background)
            shap_values = explainer(X_transformed).values

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap_abs = np.abs(shap_values).mean(axis=0)
        length = min(len(feature_names), len(shap_abs))

        shap_importance = pd.DataFrame({
            "feature": feature_names[:length],
            "mean_abs_shap": shap_abs[:length],
        }).sort_values("mean_abs_shap", ascending=False)
        shap_importance.to_csv(shap_dir / "global_shap_feature_importance.csv", index=False)

        plt.figure()
        shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, show=False)
        plt.tight_layout()
        plt.savefig(shap_dir / "shap_summary_plot.png", dpi=160, bbox_inches="tight")
        plt.close()

        plt.figure()
        shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, plot_type="bar", show=False)
        plt.tight_layout()
        plt.savefig(shap_dir / "shap_bar_plot.png", dpi=160, bbox_inches="tight")
        plt.close()

        logger.info("SHAP reports generated.")
        return shap_importance

    except Exception as exc:
        logger.exception("Failed to generate SHAP reports: %s", exc)
        (shap_dir / "shap_error.txt").write_text(str(exc), encoding="utf-8")
        return None


def generate_business_insights(
    df: pd.DataFrame,
    output_dir: Path,
    logger: logging.Logger,
) -> None:
    report_dir = output_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    insights = []
    insights.append("# Business Insights Report\n")
    insights.append(f"Generated at: {datetime.now()}\n\n")

    if "warranty_left_days" in df.columns and TARGET in df.columns:
        corr = df["warranty_left_days"].corr(df[TARGET])
        insights.append(f"Warranty vs resale value correlation: {corr:.4f}\n")

    if "crack_severity" in df.columns and TARGET in df.columns:
        corr = df["crack_severity"].corr(df[TARGET])
        insights.append(f"Crack severity vs resale value correlation: {corr:.4f}\n")

    if "condition_score" in df.columns and TARGET in df.columns:
        corr = df["condition_score"].corr(df[TARGET])
        insights.append(f"Condition score vs resale value correlation: {corr:.4f}\n")

    if {"product_category", "purchase_age_days", TARGET, "current_market_price"}.issubset(df.columns):
        temp = df.copy()
        temp["resale_to_market_pct"] = safe_divide(temp[TARGET], temp["current_market_price"]) * 100
        category_retention = (
            temp.groupby("product_category")
            .agg(
                avg_price_retention_pct=("resale_to_market_pct", "mean"),
                avg_age_days=("purchase_age_days", "mean"),
                avg_condition_score=("condition_score", "mean"),
                count=(TARGET, "count"),
            )
            .sort_values("avg_price_retention_pct", ascending=False)
        )
        category_retention.to_csv(report_dir / "category_value_retention.csv")
        insights.append("\nCategories retaining value longest:\n")
        insights.append(str(category_retention.head(5)))
        insights.append("\n\nCategories depreciating fastest:\n")
        insights.append(str(category_retention.tail(5)))

    if {"condition_score", TARGET}.issubset(df.columns):
        df["condition_bucket"] = pd.cut(
            df["condition_score"],
            bins=[-1, 40, 60, 75, 85, 100],
            labels=["Poor", "Fair", "Good", "Very Good", "Excellent"],
        )
        condition_impact = df.groupby("condition_bucket")[TARGET].mean()
        condition_impact.to_csv(report_dir / "condition_score_price_impact.csv")
        insights.append("\n\nImpact of condition score on price:\n")
        insights.append(str(condition_impact))

    (report_dir / "business_insights_report.md").write_text("\n".join(insights), encoding="utf-8")
    logger.info("Business insights report saved.")


class ResalePriceInferenceEngine:
    """
    Reusable inference and XAI wrapper.

    This object is saved as part of production artifacts and exposes:
        predict_resale_price(product_data)
        explain_prediction(product_data)
    """

    def __init__(
        self,
        model: Pipeline,
        selected_features: List[str],
        train_feature_frame: pd.DataFrame,
        train_target: pd.Series,
        shap_enabled: bool = True,
    ) -> None:
        self.model = model
        self.selected_features = selected_features
        self.feature_engineer = FeatureEngineer()
        self.train_feature_frame = train_feature_frame[selected_features].copy()
        self.train_target = train_target.copy()
        self.shap_enabled = shap_enabled and SHAP_AVAILABLE

        self.transformed_train = self.model.named_steps["preprocessor"].transform(self.train_feature_frame)
        self.nn = NearestNeighbors(n_neighbors=min(10, len(self.transformed_train)), metric="euclidean")
        self.nn.fit(self.transformed_train)

        train_preds = self.model.predict(self.train_feature_frame)
        self.train_mae = float(mean_absolute_error(self.train_target, train_preds))
        self.target_std = float(np.std(self.train_target)) if np.std(self.train_target) > 0 else 1.0

    def _prepare_input(self, product_data: Dict[str, Any]) -> pd.DataFrame:
        raw = pd.DataFrame([product_data])
        engineered = self.feature_engineer.transform(raw)
        for col in self.selected_features:
            if col not in engineered.columns:
                engineered[col] = 0
        return engineered[self.selected_features]

    def _confidence_score(self, X_prepared: pd.DataFrame, prediction: float) -> float:
        transformed = self.model.named_steps["preprocessor"].transform(X_prepared)
        distances, _ = self.nn.kneighbors(transformed)
        avg_distance = float(np.mean(distances))

        similarity_score = 100.0 * math.exp(-avg_distance / max(1.0, math.sqrt(transformed.shape[1])))

        provided_count = sum(
            1 for c in self.selected_features
            if c in X_prepared.columns and pd.notna(X_prepared.iloc[0][c])
        )
        coverage_score = 100.0 * provided_count / max(1, len(self.selected_features))

        uncertainty_penalty = min(45.0, (self.train_mae / max(abs(prediction), 1.0)) * 100.0)

        confidence = 0.55 * similarity_score + 0.25 * coverage_score + 0.20 * (100.0 - uncertainty_penalty)
        return float(np.clip(confidence, 5.0, 99.0))

    def _local_shap_factors(self, X_prepared: pd.DataFrame, top_k: int = 6) -> Tuple[List[str], List[str], Dict[str, float]]:
        if not self.shap_enabled:
            return [], [], {}

        try:
            preprocessor = self.model.named_steps["preprocessor"]
            regressor = self.model.named_steps["model"]
            transformed = preprocessor.transform(X_prepared)
            feature_names = get_transformed_feature_names(self.model)

            try:
                explainer = shap.TreeExplainer(regressor)
                shap_values = explainer.shap_values(transformed)
            except Exception:
                background = self.transformed_train[: min(200, len(self.transformed_train))]
                explainer = shap.Explainer(regressor.predict, background)
                shap_values = explainer(transformed).values

            if isinstance(shap_values, list):
                shap_values = shap_values[0]

            row_values = np.ravel(shap_values[0])
            pairs = list(zip(feature_names, row_values))
            pairs = sorted(pairs, key=lambda x: abs(x[1]), reverse=True)

            positives = [f"{name}: +₹{value:,.0f}" for name, value in pairs if value > 0][:top_k]
            negatives = [f"{name}: -₹{abs(value):,.0f}" for name, value in pairs if value < 0][:top_k]
            shap_dict = {name: float(value) for name, value in pairs[:30]}

            return positives, negatives, shap_dict
        except Exception:
            return [], [], {}

    def predict_resale_price(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        X_prepared = self._prepare_input(product_data)
        pred = float(self.model.predict(X_prepared)[0])
        pred = max(0.0, pred)

        current_market_price = float(product_data.get("current_market_price", 0) or 0)
        price_pct = (pred / current_market_price * 100.0) if current_market_price > 0 else None

        confidence = self._confidence_score(X_prepared, pred)
        positives, negatives, _ = self._local_shap_factors(X_prepared)

        return {
            "predicted_resale_price": round(pred, 2),
            "confidence_score": round(confidence, 2),
            "price_percentage_of_market": round(price_pct, 2) if price_pct is not None else None,
            "top_positive_factors": positives,
            "top_negative_factors": negatives,
        }

    def explain_prediction(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        X_prepared = self._prepare_input(product_data)
        pred = float(self.model.predict(X_prepared)[0])
        pred = max(0.0, pred)
        confidence = self._confidence_score(X_prepared, pred)
        positives, negatives, shap_values = self._local_shap_factors(X_prepared)

        return {
            "predicted_resale_price": round(pred, 2),
            "confidence_score": round(confidence, 2),
            "top_positive_factors": positives,
            "top_negative_factors": negatives,
            "shap_values": shap_values,
        }


def write_training_report(
    output_dir: Path,
    best_name: str,
    comparison_df: pd.DataFrame,
    feature_reasoning: Dict[str, Any],
    search_details: Dict[str, Any],
    logger: logging.Logger,
) -> None:
    lines = []
    lines.append("RESALE PRICE MODEL TRAINING REPORT")
    lines.append("=" * 80)
    lines.append(f"Generated at: {datetime.now()}")
    lines.append(f"Best model: {best_name}")
    lines.append("\nMODEL COMPARISON")
    lines.append(comparison_df.to_string(index=False))
    lines.append("\n\nFEATURE SELECTION SUMMARY")
    lines.append(json.dumps(feature_reasoning, indent=2, default=str))
    lines.append("\n\nHYPERPARAMETER SEARCH DETAILS")
    lines.append(json.dumps(search_details, indent=2, default=str))

    (output_dir / "training_report.txt").write_text("\n".join(lines), encoding="utf-8")
    logger.info("Training report written.")


def train_pipeline(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(output_dir)

    logger.info("Starting resale price model pipeline.")
    logger.info("Arguments: %s", vars(args))

    df_raw = load_csv(Path(args.data_path), logger)

    generate_eda_report(df_raw, output_dir, logger)

    df_clean = clean_and_validate(df_raw, logger)
    df_clean.to_csv(output_dir / "cleaned_dataset.csv", index=False)

    feature_engineer = FeatureEngineer()
    df_engineered = feature_engineer.transform(df_clean)
    df_engineered[TARGET] = df_clean[TARGET].values

    feature_reasoning = analyze_feature_selection(
        engineered_df=df_engineered.drop(columns=[TARGET], errors="ignore"),
        target=df_engineered[TARGET],
        output_dir=output_dir,
        logger=logger,
    )

    selected_features = feature_reasoning["selected_features"]

    X = df_engineered[selected_features]
    y = df_engineered[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )

    preprocessor = build_preprocessor(df_engineered, selected_features)

    best_name, best_model, comparison_df, search_details = train_models(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        preprocessor=preprocessor,
        output_dir=output_dir,
        logger=logger,
        fast_mode=args.fast_mode,
    )

    best_metrics = comparison_df.iloc[0].to_dict()
    save_json(best_metrics, output_dir / "best_model_metrics.json")

    generate_evaluation_plots(
        best_model=best_model,
        model_name=best_name,
        X_test=X_test,
        y_test=y_test,
        comparison_df=comparison_df,
        output_dir=output_dir,
        logger=logger,
    )

    feature_importance_df = generate_feature_importance_report(best_model, output_dir, logger)

    shap_importance_df = generate_shap_reports(best_model, X_train, X_test, output_dir, logger)

    generate_business_insights(df_engineered, output_dir, logger)

    inference_engine = ResalePriceInferenceEngine(
        model=best_model,
        selected_features=selected_features,
        train_feature_frame=X_train,
        train_target=y_train,
        shap_enabled=True,
    )

    metadata = {
        "created_at": datetime.now().isoformat(),
        "target": TARGET,
        "best_model_name": best_name,
        "random_state": RANDOM_STATE,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "selected_features": selected_features,
        "excluded_features": BASE_EXCLUDED_FEATURES,
        "available_optional_models": {
            "xgboost": XGBOOST_AVAILABLE,
            "lightgbm": LIGHTGBM_AVAILABLE,
            "catboost": CATBOOST_AVAILABLE,
            "shap": SHAP_AVAILABLE,
        },
        "business_categories_optimized": sorted(SUPPORTED_CATEGORIES),
    }

    save_pickle(best_model, output_dir / "resale_price_model.pkl")
    save_pickle(best_model.named_steps["preprocessor"], output_dir / "preprocessing_pipeline.pkl")
    save_pickle(inference_engine, output_dir / "resale_price_inference_engine.pkl")
    save_json(selected_features, output_dir / "feature_columns.json")
    save_json(metadata, output_dir / "model_metadata.json")

    write_training_report(
        output_dir=output_dir,
        best_name=best_name,
        comparison_df=comparison_df,
        feature_reasoning=feature_reasoning,
        search_details=search_details,
        logger=logger,
    )

    logger.info("Pipeline completed successfully.")
    logger.info("Artifacts saved to: %s", output_dir.resolve())

    print("\nTraining completed successfully.")
    print(f"Best model: {best_name}")
    print(f"Best metrics: {json.dumps(best_metrics, indent=2, default=str)}")
    print(f"Artifacts saved to: {output_dir.resolve()}")


def load_inference_engine(artifact_dir: str | Path) -> ResalePriceInferenceEngine:
    with open(Path(artifact_dir) / "resale_price_inference_engine.pkl", "rb") as f:
        return pickle.load(f)


def predict_resale_price(product_data: Dict[str, Any], artifact_dir: str | Path = "artifacts") -> Dict[str, Any]:
    engine = load_inference_engine(artifact_dir)
    return engine.predict_resale_price(product_data)


def explain_prediction(product_data: Dict[str, Any], artifact_dir: str | Path = "artifacts") -> Dict[str, Any]:
    engine = load_inference_engine(artifact_dir)
    return engine.explain_prediction(product_data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train resale price prediction model.")
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to input CSV dataset.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="artifacts",
        help="Directory to save models, reports, plots, and metadata.",
    )
    parser.add_argument(
        "--fast_mode",
        action="store_true",
        help="Use smaller hyperparameter searches for hackathon demos.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    train_pipeline(parse_args())
