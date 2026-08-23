import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_installments
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Installment Payment Analysis", page_icon="🏦", layout="wide")
st.title("💸 17 · Installment Payment Analysis ")

inst = load_installments()

# Simple feature engineering
inst = inst.copy()
if "DAYS_ENTRY_PAYMENT" in inst.columns and "DAYS_INSTALMENT" in inst.columns:
    inst["PAYMENT_DELAY"] = inst["DAYS_ENTRY_PAYMENT"] - inst["DAYS_INSTALMENT"]
if "AMT_PAYMENT" in inst.columns and "AMT_INSTALMENT" in inst.columns:
    inst["PAYMENT_DIFF"] = inst["AMT_PAYMENT"] - inst["AMT_INSTALMENT"]

st.subheader("Installment Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Total Installments", format_number(len(inst)))
c2.metric("Unique Customers", format_number(inst["SK_ID_CURR"].nunique()) if "SK_ID_CURR" in inst.columns else "N/A")
c3.metric("Average Installment", format_number(inst["AMT_INSTALMENT"].mean()) if "AMT_INSTALMENT" in inst.columns else "N/A")

st.divider()

if "PAYMENT_DELAY" in inst.columns:
    st.subheader("Payment Delay Distribution")
    fig1 = px.histogram(inst, x="PAYMENT_DELAY", nbins=40)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

    late_pct = (inst["PAYMENT_DELAY"] > 0).mean()
    st.metric("Late Payment %", f"{late_pct*100:.1f}%")

if "PAYMENT_DIFF" in inst.columns:
    st.subheader("Payment Difference Distribution")
    fig2 = px.histogram(inst, x="PAYMENT_DIFF", nbins=40)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "AMT_INSTALMENT" in inst.columns and "AMT_PAYMENT" in inst.columns:
    st.subheader("Scheduled vs Actual Payment")
    sample = inst.sample(n=min(2000, len(inst)), random_state=42)
    fig3 = px.scatter(sample, x="AMT_INSTALMENT", y="AMT_PAYMENT", opacity=0.5)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("Key Observations")
st.write("- Payment delay is a strong behavioural signal.")
st.write("- Underpayment and late payment should be monitored.")
st.write("- This page is one of the most important for risk EDA.")

st.subheader("Recommendations")
st.write("1. Create early-warning flags for repeated late payments.")
st.write("2. Track customers whose delays are increasing.")
st.write("3. Combine with bureau and credit-card behaviour.")