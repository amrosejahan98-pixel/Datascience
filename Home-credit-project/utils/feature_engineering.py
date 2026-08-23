import pandas as pd
import numpy as np

def create_core_features(df):
    df = df.copy()
    
    # Age in years
    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = (-df["DAYS_BIRTH"] / 365).round(1)
    
    # Employment years
    if "DAYS_EMPLOYED" in df.columns:
        df["EMPLOYMENT_YEARS"] = (-df["DAYS_EMPLOYED"] / 365).round(1)
    
    # Credit to Income ratio
    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["CREDIT_TO_INCOME"] = (df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]).round(2)
    
    # Annuity to Income ratio
    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_TO_INCOME"] = (df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]).round(2)
    
    return df