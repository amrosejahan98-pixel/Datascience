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

st.set_page_config(page_title="Income Analysis", page_icon="🏦", layout="wide")
st.title("💵 06 · Income Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Income Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Average Income", format_number(filtered["AMT_INCOME_TOTAL"].mean()))
c2.metric("Median Income", format_number(filtered["AMT_INCOME_TOTAL"].median()))
c3.metric("Maximum Income", format_number(filtered["AMT_INCOME_TOTAL"].max()))
c4.metric("Minimum Income", format_number(filtered["AMT_INCOME_TOTAL"].min()))

st.divider()

st.subheader("Income Distribution")
fig1 = px.histogram(filtered, x="AMT_INCOME_TOTAL", nbins=40)
st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "INCOME_GROUP" in filtered.columns:
    st.subheader("Income Group Distribution")
    ig = filtered["INCOME_GROUP"].value_counts().reset_index()
    ig.columns = ["Income Group", "Count"]
    fig2 = px.bar(ig, x="Income Group", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

st.subheader("Income vs Credit")
sample = filtered.sample(n=min(2000, len(filtered)), random_state=42)
fig3 = px.scatter(sample, x="AMT_INCOME_TOTAL", y="AMT_CREDIT", opacity=0.5)
st.plotly_chart(apply_layout(fig3), use_container_width=True)

if "NAME_EDUCATION_TYPE" in filtered.columns:
    st.subheader("Income by Education")
    fig4 = px.box(filtered, x="NAME_EDUCATION_TYPE", y="AMT_INCOME_TOTAL")
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Average income: **{format_number(filtered['AMT_INCOME_TOTAL'].mean())}**")
st.write(f"- Median income: **{format_number(filtered['AMT_INCOME_TOTAL'].median())}**")
st.write("- Higher education generally links to higher income.")

st.subheader("Recommendations")
st.write("1. Review credit limits for very low income groups.")
st.write("2. Check default rates by income group on later pages.")