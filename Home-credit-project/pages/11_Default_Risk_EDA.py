import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_application
from utils.preprocessing import clean_application
from utils.feature_engineering import create_core_features
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number, format_percent
from utils.charts import apply_layout

st.set_page_config(page_title="Default Risk EDA", page_icon="🏦", layout="wide")
st.title("⚠️ 11 · Default Risk EDA ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

default_cnt = int(filtered["TARGET"].sum())
total = len(filtered)
default_rate = default_cnt / total if total > 0 else 0

st.subheader("Default Risk Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Default Customers", format_number(default_cnt))
c2.metric("Non-Default Customers", format_number(total - default_cnt))
c3.metric("Default Rate", format_percent(default_rate))
c4.metric("Total Applications", format_number(total))

st.divider()

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("TARGET Distribution")
    tc = filtered["TARGET"].value_counts().reset_index()
    tc.columns = ["TARGET", "Count"]
    tc["Label"] = tc["TARGET"].map({0: "Non-Default", 1: "Default"})
    fig1 = px.bar(tc, x="Label", y="Count", color="Label", text_auto=True)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

with col_b:
    st.subheader("Default Percentage")
    fig2 = go.Figure(data=[go.Pie(labels=["Non-Default", "Default"], values=[total-default_cnt, default_cnt], hole=0.4)])
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "AGE_GROUP" in filtered.columns:
    st.subheader("Default Rate by Age Group")
    age_def = filtered.groupby("AGE_GROUP")["TARGET"].mean().reset_index()
    age_def.columns = ["Age Group", "Default Rate"]
    fig3 = px.bar(age_def, x="Age Group", y="Default Rate", text_auto=".1%")
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

if "NAME_EDUCATION_TYPE" in filtered.columns:
    st.subheader("Default Rate by Education")
    edu_def = filtered.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().reset_index()
    edu_def.columns = ["Education", "Default Rate"]
    fig4 = px.bar(edu_def, x="Default Rate", y="Education", orientation="h", text_auto=".1%")
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Overall default rate: **{format_percent(default_rate)}**")
st.write("- Default rate is different across age and education groups.")
st.write("- Always compare **rate**, not only number of defaults.")

st.subheader("Recommendations")
st.write("1. Focus monitoring on high default-rate segments.")
st.write("2. Do not judge risk only by count of defaults.")