"""
Data cleaning and basic preprocessing utilities.
"""

import pandas as pd
import numpy as np


def clean_application(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning for application_train:
    - Fix known invalid values (DAYS_EMPLOYED = 365243)
    - Ensure correct dtypes for key columns
    """
    df = df.copy()

    # DAYS_EMPLOYED anomaly: 365243 means "unemployed / pensioner / missing"
    if "DAYS_EMPLOYED" in df.columns:
        df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, np.nan)

    # Ensure TARGET is int
    if "TARGET" in df.columns:
        df["TARGET"] = df["TARGET"].astype(int)

    # Convert binary flags to int where possible
    flag_cols = [c for c in df.columns if c.startswith("FLAG_")]
    for col in flag_cols:
        if df[col].dtype == object:
            df[col] = df[col].map({"Y": 1, "N": 0, "Yes": 1, "No": 0}).fillna(df[col])

    return df


def handle_missing(df: pd.DataFrame, strategy: str = "report") -> pd.DataFrame:
    """
    Simple missing-value helper.
    strategy = 'report'  → only returns missing summary (does not modify)
    strategy = 'median'  → fill numeric with median
    strategy = 'mode'    → fill categorical with mode
    """
    if strategy == "report":
        miss = df.isnull().sum()
        miss_pct = (miss / len(df) * 100).round(2)
        report = pd.DataFrame({
            "column": miss.index,
            "missing_count": miss.values,
            "missing_pct": miss_pct.values
        })
        return report[report["missing_count"] > 0].sort_values("missing_pct", ascending=False)

    df = df.copy()
    if strategy == "median":
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
    elif strategy == "mode":
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col] = df[col].fillna(mode_val[0])
    return df


def get_data_quality_summary(df: pd.DataFrame) -> dict:
    """Return a dictionary of high-level data quality metrics."""
    n_rows, n_cols = df.shape
    n_numeric = len(df.select_dtypes(include=[np.number]).columns)
    n_categorical = len(df.select_dtypes(include=["object", "category"]).columns)
    missing_cells = int(df.isnull().sum().sum())
    missing_pct = round(missing_cells / (n_rows * n_cols) * 100, 2)
    duplicate_rows = int(df.duplicated().sum())
    memory_mb = round(df.memory_usage(deep=True).sum() / 1024**2, 2)

    unique_customers = df["SK_ID_CURR"].nunique() if "SK_ID_CURR" in df.columns else n_rows

    return {
        "rows": n_rows,
        "columns": n_cols,
        "numeric_cols": n_numeric,
        "categorical_cols": n_categorical,
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
        "memory_mb": memory_mb,
        "unique_customers": unique_customers,
    }