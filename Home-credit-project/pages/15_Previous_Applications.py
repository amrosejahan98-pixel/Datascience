import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_previous_application
from utils.metrics import format_number, format_percent
from utils.charts import apply_layout

st.set_page_config(page_title="Previous Applications", page_icon="🏦", layout="wide")
st.title("📂 15 · Previous Applications ")

prev = load_previous_application()

st.subheader("Previous Application Metrics")
total = len(prev)
approved = (prev["NAME_CONTRACT_STATUS"] == "Approved").sum() if "NAME_CONTRACT_STATUS" in prev.columns else 0
refused = (prev["NAME_CONTRACT_STATUS"] == "Refused").sum() if "NAME_CONTRACT_STATUS" in prev.columns else 0
approval_rate = approved / total if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Previous Applications", format_number(total))
c2.metric("Approved", format_number(approved))
c3.metric("Refused", format_number(refused))
c4.metric("Approval Rate", format_percent(approval_rate))

st.divider()

if "NAME_CONTRACT_STATUS" in prev.columns:
    st.subheader("Application Status")
    status = prev["NAME_CONTRACT_STATUS"].value_counts().reset_index()
    status.columns = ["Status", "Count"]
    fig1 = px.bar(status, x="Status", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "NAME_CONTRACT_TYPE" in prev.columns:
    st.subheader("Previous Contract Types")
    ctype = prev["NAME_CONTRACT_TYPE"].value_counts().reset_index()
    ctype.columns = ["Contract Type", "Count"]
    fig2 = px.bar(ctype, x="Contract Type", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "NAME_CLIENT_TYPE" in prev.columns:
    st.subheader("Client Type")
    client = prev["NAME_CLIENT_TYPE"].value_counts().reset_index()
    client.columns = ["Client Type", "Count"]
    fig3 = px.bar(client, x="Client Type", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Total previous applications: **{format_number(total)}**")
st.write(f"- Approval rate: **{format_percent(approval_rate)}**")
st.write("- Past refusals can be an important signal.")

st.subheader("Recommendations")
st.write("1. Review customers with many past refusals.")
st.write("2. Compare approved vs refused application patterns.")
st.write("3. Track repeat customers carefully.")