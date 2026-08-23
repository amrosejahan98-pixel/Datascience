import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add project folder to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_application
from utils.preprocessing import clean_application
from utils.feature_engineering import create_core_features
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number, format_percent
from utils.charts import apply_layout

st.set_page_config(page_title="Executive Overview", page_icon="🏦", layout="wide")

st.title("🏦 01 · Executive Portfolio Overview ")

# Load data
df = load_application()
df = clean_application(df)
df = create_core_features(df)

# Sidebar filters
filtered = apply_sidebar_filters(df)

# ===================== KPI CARDS =====================
st.subheader("Key Portfolio Metrics")

total_customers = filtered["SK_ID_CURR"].nunique()
total_apps = len(filtered)
default_cnt = filtered["TARGET"].sum()
non_default_cnt = total_apps - default_cnt
default_rate = default_cnt / total_apps

avg_credit = filtered["AMT_CREDIT"].mean()
avg_income = filtered["AMT_INCOME_TOTAL"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", format_number(total_customers))
col2.metric("Total Applications", format_number(total_apps))
col3.metric("Default Customers", format_number(default_cnt))
col4.metric("Default Rate", format_percent(default_rate))

col5, col6, col7, col8 = st.columns(4)
col5.metric("Non-Default Customers", format_number(non_default_cnt))
col6.metric("Average Credit", format_number(avg_credit))
col7.metric("Average Income", format_number(avg_income))
col8.metric("Total Credit", format_number(filtered["AMT_CREDIT"].sum()))

st.divider()

# ===================== CHARTS =====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Default vs Non-Default")
    target_counts = filtered["TARGET"].value_counts().reset_index()
    target_counts.columns = ["TARGET", "Count"]
    target_counts["Label"] = target_counts["TARGET"].map({0: "Non-Default", 1: "Default"})
    
    fig1 = px.bar(target_counts, x="Label", y="Count", color="Label", text_auto=True)
    fig1 = apply_layout(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Default Percentage")
    fig2 = go.Figure(data=[go.Pie(
        labels=["Non-Default", "Default"],
        values=[non_default_cnt, default_cnt],
        hole=0.4
    )])
    fig2 = apply_layout(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# Contract Type
st.subheader("Applications by Contract Type")
contract_cnt = filtered["NAME_CONTRACT_TYPE"].value_counts().reset_index()
contract_cnt.columns = ["Contract Type", "Count"]
fig3 = px.bar(contract_cnt, x="Contract Type", y="Count", text_auto=True)
fig3 = apply_layout(fig3)
st.plotly_chart(fig3, use_container_width=True)

# Credit Distribution
st.subheader("Credit Amount Distribution")
fig4 = px.histogram(filtered, x="AMT_CREDIT", nbins=30)
fig4 = apply_layout(fig4)
st.plotly_chart(fig4, use_container_width=True)

# ===================== INSIGHTS =====================
st.subheader("Key Observations")
st.write(f"- Total customers in portfolio: **{format_number(total_customers)}**")
st.write(f"- Overall default rate: **{format_percent(default_rate)}**")
st.write(f"- Average credit amount: **{format_number(avg_credit)}**")
st.write(f"- Average customer income: **{format_number(avg_income)}**")

st.subheader("Recommendations")
st.write("1. Monitor the default rate closely.")
st.write("2. Review high credit amount applications carefully.")
st.write("3. Focus on customer segments with higher default rates.")
