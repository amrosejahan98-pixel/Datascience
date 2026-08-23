import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_bureau
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Bureau Credit History", page_icon="🏦", layout="wide")
st.title("🏛️ 13 · Bureau Credit History ")

bureau = load_bureau()

st.subheader("Bureau Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Bureau Records", format_number(len(bureau)))
c2.metric("Unique Customers", format_number(bureau["SK_ID_CURR"].nunique()))
c3.metric("Active Credits", format_number((bureau["CREDIT_ACTIVE"] == "Active").sum()) if "CREDIT_ACTIVE" in bureau.columns else "N/A")
c4.metric("Closed Credits", format_number((bureau["CREDIT_ACTIVE"] == "Closed").sum()) if "CREDIT_ACTIVE" in bureau.columns else "N/A")

st.divider()

if "CREDIT_ACTIVE" in bureau.columns:
    st.subheader("Active vs Closed Loans")
    status = bureau["CREDIT_ACTIVE"].value_counts().reset_index()
    status.columns = ["Status", "Count"]
    fig1 = px.bar(status, x="Status", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "CREDIT_TYPE" in bureau.columns:
    st.subheader("Credit Type Distribution")
    ctype = bureau["CREDIT_TYPE"].value_counts().head(10).reset_index()
    ctype.columns = ["Credit Type", "Count"]
    fig2 = px.bar(ctype, x="Count", y="Credit Type", orientation="h", text_auto=True)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "AMT_CREDIT_SUM" in bureau.columns:
    st.subheader("Bureau Credit Amount Distribution")
    fig3 = px.histogram(bureau, x="AMT_CREDIT_SUM", nbins=40)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Total bureau records: **{format_number(len(bureau))}**")
st.write("- Customers may have multiple external loans.")
st.write("- Active and closed credits give useful history signals.")

st.subheader("Recommendations")
st.write("1. Review customers with many active external loans.")
st.write("2. Check overdue amounts carefully.")
st.write("3. Combine bureau data with internal repayment behaviour.")