import streamlit as st
import pandas as pd
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

st.set_page_config(page_title="Risk Factor Analysis", page_icon="🏦", layout="wide")
st.title("🔎 12 · Risk Factor Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Risk Factor Overview")
st.write("This page shows observed relationships between key variables and default.")

if "AGE_GROUP" in filtered.columns:
    st.subheader("Age Group vs Default Rate")
    age_def = filtered.groupby("AGE_GROUP")["TARGET"].mean().reset_index()
    fig1 = px.bar(age_def, x="AGE_GROUP", y="TARGET", text_auto=".1%")
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "INCOME_GROUP" in filtered.columns:
    st.subheader("Income Group vs Default Rate")
    inc_def = filtered.groupby("INCOME_GROUP")["TARGET"].mean().reset_index()
    fig2 = px.bar(inc_def, x="INCOME_GROUP", y="TARGET", text_auto=".1%")
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "CREDIT_TO_INCOME" in filtered.columns:
    st.subheader("Credit-to-Income vs Default")
    fig3 = px.box(filtered, x="TARGET", y="CREDIT_TO_INCOME")
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("Correlation (Numeric Columns)")
num_cols = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AGE_YEARS", "CREDIT_TO_INCOME", "TARGET"]
num_cols = [c for c in num_cols if c in filtered.columns]
corr = filtered[num_cols].corr()
fig4 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r")
st.plotly_chart(apply_layout(fig4, height=500), use_container_width=True)

st.subheader("Key Observations")
st.write("- Some groups show higher observed default rates.")
st.write("- Correlation does **not** mean causation.")
st.write("- Credit-to-Income can be an important risk signal.")

st.subheader("Recommendations")
st.write("1. Monitor high Credit-to-Income customers.")
st.write("2. Review segments with higher default rates.")
st.write("3. Use these findings for policy discussion, not prediction.")