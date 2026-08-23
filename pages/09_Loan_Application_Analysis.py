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

st.set_page_config(page_title="Loan Application Analysis", page_icon="🏦", layout="wide")
st.title("📝 09 · Current Loan Application Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Loan Application Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Applications", format_number(len(filtered)))
c2.metric("Average Credit", format_number(filtered["AMT_CREDIT"].mean()))
c3.metric("Median Credit", format_number(filtered["AMT_CREDIT"].median()))
c4.metric("Average Annuity", format_number(filtered["AMT_ANNUITY"].mean()) if "AMT_ANNUITY" in filtered.columns else "N/A")

st.divider()

st.subheader("Applications by Contract Type")
cc = filtered["NAME_CONTRACT_TYPE"].value_counts().reset_index()
cc.columns = ["Contract Type", "Count"]
fig1 = px.bar(cc, x="Contract Type", y="Count", text_auto=True)
st.plotly_chart(apply_layout(fig1), use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Credit Amount Distribution")
    fig2 = px.histogram(filtered, x="AMT_CREDIT", nbins=40)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

with col_b:
    if "AMT_ANNUITY" in filtered.columns:
        st.subheader("Annuity Distribution")
        fig3 = px.histogram(filtered, x="AMT_ANNUITY", nbins=40)
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

if "AMT_GOODS_PRICE" in filtered.columns:
    st.subheader("Credit vs Goods Price")
    sample = filtered.sample(n=min(2000, len(filtered)), random_state=42)
    fig4 = px.scatter(sample, x="AMT_GOODS_PRICE", y="AMT_CREDIT", opacity=0.5)
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Total applications: **{format_number(len(filtered))}**")
st.write(f"- Average credit: **{format_number(filtered['AMT_CREDIT'].mean())}**")
st.write("- Most applications are Cash loans.")

st.subheader("Recommendations")
st.write("1. Monitor the most popular contract type.")
st.write("2. Check unusual credit vs goods price patterns.")