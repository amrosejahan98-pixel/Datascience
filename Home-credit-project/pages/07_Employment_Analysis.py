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

st.set_page_config(page_title="Employment Analysis", page_icon="🏦", layout="wide")
st.title("💼 07 · Employment Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Employment Metrics")
avg_emp = filtered["EMPLOYMENT_YEARS"].mean() if "EMPLOYMENT_YEARS" in filtered.columns else 0
c1, c2, c3 = st.columns(3)
c1.metric("Average Employment Years", f"{avg_emp:.1f}")
c2.metric("Records", format_number(len(filtered)))
c3.metric("Customers", format_number(filtered["SK_ID_CURR"].nunique()))

st.divider()

if "EMPLOYMENT_YEARS" in filtered.columns:
    st.subheader("Employment Years Distribution")
    fig1 = px.histogram(filtered, x="EMPLOYMENT_YEARS", nbins=30)
    st.plotly_chart(apply_layout(fig1), use_container_width=True)

if "OCCUPATION_TYPE" in filtered.columns:
    st.subheader("Top Occupations")
    occ = filtered["OCCUPATION_TYPE"].value_counts().head(15).reset_index()
    occ.columns = ["Occupation", "Count"]
    fig2 = px.bar(occ, x="Count", y="Occupation", orientation="h", text_auto=True)
    st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "ORGANIZATION_TYPE" in filtered.columns:
    st.subheader("Top Organization Types")
    org = filtered["ORGANIZATION_TYPE"].value_counts().head(15).reset_index()
    org.columns = ["Organization", "Count"]
    fig3 = px.bar(org, x="Count", y="Organization", orientation="h", text_auto=True)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Average employment years: **{avg_emp:.1f}**")
st.write("- Some customers have very short or missing employment history.")

st.subheader("Recommendations")
st.write("1. Treat missing employment carefully.")
st.write("2. Check default rates by occupation on later pages.")