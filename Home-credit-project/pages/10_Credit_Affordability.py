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

st.set_page_config(page_title="Credit Affordability", page_icon="🏦", layout="wide")
st.title("💳 10 · Credit Affordability Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Affordability Metrics")

avg_cti = filtered["CREDIT_TO_INCOME"].mean() if "CREDIT_TO_INCOME" in filtered.columns else 0
avg_ati = filtered["ANNUITY_TO_INCOME"].mean() if "ANNUITY_TO_INCOME" in filtered.columns else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Credit-to-Income", f"{avg_cti:.2f}")
c2.metric("Avg Annuity-to-Income", f"{avg_ati:.2f}")
c3.metric("Customers", format_number(filtered["SK_ID_CURR"].nunique()))
c4.metric("Applications", format_number(len(filtered)))

st.divider()

if "CREDIT_TO_INCOME" in filtered.columns:
    st.subheader("Credit-to-Income Distribution")
    fig1 = px.histogram(filtered, x="CREDIT_TO_INCOME", nbins=40)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "ANNUITY_TO_INCOME" in filtered.columns:
    st.subheader("Annuity-to-Income Distribution")
    fig2 = px.histogram(filtered, x="ANNUITY_TO_INCOME", nbins=40)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

st.subheader("Income vs Credit")
sample = filtered.sample(n=min(2000, len(filtered)), random_state=42)
fig3 = px.scatter(sample, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", opacity=0.5)
st.plotly_chart(apply_layout(fig3), use_container_width=True)

if "CREDIT_TO_INCOME" in filtered.columns:
    st.subheader("Credit-to-Income by Default Status")
    fig4 = px.box(filtered, x="TARGET", y="CREDIT_TO_INCOME")
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Average Credit-to-Income ratio: **{avg_cti:.2f}**")
st.write(f"- Average Annuity-to-Income ratio: **{avg_ati:.2f}**")
st.write("- Higher ratios may indicate higher repayment pressure.")

st.subheader("Recommendations")
st.write("1. Review customers with very high Credit-to-Income ratio.")
st.write("2. Monitor high Annuity burden customers.")
st.write("3. Set internal affordability guidelines.")