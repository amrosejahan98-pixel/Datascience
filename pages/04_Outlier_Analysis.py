import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_application
from utils.preprocessing import clean_application
from utils.feature_engineering import create_core_features
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Outlier Analysis", page_icon="🏦", layout="wide")
st.title("📈 04 · Outlier & Distribution Analysis ")

# Load data
df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

# ===================== KPI CARDS =====================
st.subheader("Outlier Metrics")

num_cols = filtered.select_dtypes(include=[np.number]).columns.tolist()
# Remove ID and TARGET from outlier check
check_cols = [c for c in ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE", "AGE_YEARS"] if c in filtered.columns]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Numeric Columns", format_number(len(num_cols)))
col2.metric("Max Income", format_number(filtered["AMT_INCOME_TOTAL"].max()))
col3.metric("Max Credit", format_number(filtered["AMT_CREDIT"].max()))
col4.metric("Max Annuity", format_number(filtered["AMT_ANNUITY"].max()) if "AMT_ANNUITY" in filtered.columns else "N/A")

st.divider()

# ===================== IQR OUTLIER FUNCTION =====================
def detect_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = series[(series < lower) | (series > upper)]
    return len(outliers), lower, upper

# ===================== CHARTS =====================
st.subheader("Income Distribution & Outliers")

col_a, col_b = st.columns(2)

with col_a:
    fig1 = px.histogram(filtered, x="AMT_INCOME_TOTAL", nbins=40)
    fig1 = apply_layout(fig1, title="Income Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = px.box(filtered, y="AMT_INCOME_TOTAL")
    fig2 = apply_layout(fig2, title="Income Box Plot (Outliers)")
    st.plotly_chart(fig2, use_container_width=True)

# Credit
st.subheader("Credit Amount Distribution & Outliers")

col_c, col_d = st.columns(2)

with col_c:
    fig3 = px.histogram(filtered, x="AMT_CREDIT", nbins=40)
    fig3 = apply_layout(fig3, title="Credit Distribution")
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    fig4 = px.box(filtered, y="AMT_CREDIT")
    fig4 = apply_layout(fig4, title="Credit Box Plot (Outliers)")
    st.plotly_chart(fig4, use_container_width=True)

# Annuity
if "AMT_ANNUITY" in filtered.columns:
    st.subheader("Annuity Distribution & Outliers")
    col_e, col_f = st.columns(2)
    
    with col_e:
        fig5 = px.histogram(filtered, x="AMT_ANNUITY", nbins=40)
        fig5 = apply_layout(fig5, title="Annuity Distribution")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col_f:
        fig6 = px.box(filtered, y="AMT_ANNUITY")
        fig6 = apply_layout(fig6, title="Annuity Box Plot")
        st.plotly_chart(fig6, use_container_width=True)

# Income vs Credit Scatter
st.subheader("Income vs Credit")
sample = filtered.sample(n=min(2000, len(filtered)), random_state=42)
fig7 = px.scatter(sample, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", opacity=0.5)
fig7 = apply_layout(fig7, title="Income vs Credit Amount")
st.plotly_chart(fig7, use_container_width=True)

# ===================== OUTLIER SUMMARY TABLE =====================
st.subheader("Outlier Summary (IQR Method)")

outlier_data = []
for col in check_cols:
    count, lower, upper = detect_outliers(filtered[col].dropna())
    outlier_data.append({
        "Column": col,
        "Outlier Count": count,
        "Lower Limit": round(lower, 2),
        "Upper Limit": round(upper, 2)
    })

outlier_df = pd.DataFrame(outlier_data)
st.dataframe(outlier_df, use_container_width=True)

# ===================== INSIGHTS =====================
st.subheader("Key Observations")
st.write("- Some customers have very high income and credit amounts.")
st.write("- Box plots show clear outliers in Income, Credit and Annuity.")
st.write("- Not all outliers are errors — some may be genuine high-value customers.")

st.subheader("Recommendations")
st.write("1. Do not automatically delete all outliers.")
st.write("2. Check if extreme values are data entry errors.")
st.write("3. Use capping (Winsorization) only when necessary.")
st.write("4. Keep true high-income / high-credit customers for analysis.")