import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_credit_card
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Credit Card Analysis", page_icon="🏦", layout="wide")
st.title("💳 18 · Credit Card Analysis ")

cc = load_credit_card()

st.subheader("Credit Card Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Total Records", format_number(len(cc)))
c2.metric("Unique Customers", format_number(cc["SK_ID_CURR"].nunique()) if "SK_ID_CURR" in cc.columns else "N/A")
c3.metric("Average Balance", format_number(cc["AMT_BALANCE"].mean()) if "AMT_BALANCE" in cc.columns else "N/A")

st.divider()

if "AMT_BALANCE" in cc.columns:
    st.subheader("Credit Balance Distribution")
    fig1 = px.histogram(cc, x="AMT_BALANCE", nbins=40)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "AMT_CREDIT_LIMIT_ACTUAL" in cc.columns:
    st.subheader("Credit Limit Distribution")
    fig2 = px.histogram(cc, x="AMT_CREDIT_LIMIT_ACTUAL", nbins=40)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "AMT_BALANCE" in cc.columns and "AMT_CREDIT_LIMIT_ACTUAL" in cc.columns:
    cc = cc.copy()
    cc["UTILIZATION"] = cc["AMT_BALANCE"] / cc["AMT_CREDIT_LIMIT_ACTUAL"].replace(0, pd.NA)
    st.subheader("Credit Utilization Distribution")
    fig3 = px.histogram(cc, x="UTILIZATION", nbins=40)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

if "SK_DPD" in cc.columns:
    st.subheader("Days Past Due (DPD)")
    fig4 = px.histogram(cc, x="SK_DPD", nbins=30)
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

st.subheader("Key Observations")
st.write("- High utilization can indicate financial pressure.")
st.write("- DPD on credit cards is an important risk signal.")
st.write("- Balance vs limit helps understand customer behaviour.")

st.subheader("Recommendations")
st.write("1. Monitor customers with very high utilization.")
st.write("2. Track credit-card DPD closely.")
st.write("3. Combine with installment late-payment data.")