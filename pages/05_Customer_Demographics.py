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
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Customer Demographics", page_icon="🏦", layout="wide")
st.title("👥 05 · Customer Demographic Analysis ")

# Load data
df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

# ===================== KPI CARDS =====================
st.subheader("Customer Profile Metrics")

avg_age = filtered["AGE_YEARS"].mean() if "AGE_YEARS" in filtered.columns else 0
median_age = filtered["AGE_YEARS"].median() if "AGE_YEARS" in filtered.columns else 0
most_gender = filtered["CODE_GENDER"].mode()[0] if "CODE_GENDER" in filtered.columns else "N/A"
most_education = filtered["NAME_EDUCATION_TYPE"].mode()[0] if "NAME_EDUCATION_TYPE" in filtered.columns else "N/A"
most_income_type = filtered["NAME_INCOME_TYPE"].mode()[0] if "NAME_INCOME_TYPE" in filtered.columns else "N/A"
most_family = filtered["NAME_FAMILY_STATUS"].mode()[0] if "NAME_FAMILY_STATUS" in filtered.columns else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Average Age", f"{avg_age:.1f} years")
col2.metric("Median Age", f"{median_age:.1f} years")
col3.metric("Most Common Gender", most_gender)

col4, col5, col6 = st.columns(3)
col4.metric("Most Common Education", most_education)
col5.metric("Most Common Income Type", most_income_type)
col6.metric("Most Common Family Status", most_family)

st.divider()

# ===================== CHARTS =====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Age Distribution")
    if "AGE_YEARS" in filtered.columns:
        fig1 = px.histogram(filtered, x="AGE_YEARS", nbins=30,color_discrete_sequence=["#C7E32B"])
        fig1 = apply_layout(fig1, title="Age Distribution")
        st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Gender Distribution")
    if "CODE_GENDER" in filtered.columns:
        gender_cnt = filtered["CODE_GENDER"].value_counts()
        fig2 = go.Figure(data=[go.Pie(
            labels=gender_cnt.index,
            values=gender_cnt.values,
            hole=0.4,
            marker=dict(colors=["#FF5733", "#2BDDE3"])
        )])
        fig2 = apply_layout(fig2, title="Gender")
        st.plotly_chart(fig2, use_container_width=True)

# Education
st.subheader("Education Distribution")
if "NAME_EDUCATION_TYPE" in filtered.columns:
    edu_cnt = filtered["NAME_EDUCATION_TYPE"].value_counts().reset_index()
    edu_cnt.columns = ["Education", "Count"]
    fig3 = px.bar(edu_cnt, x="Count", y="Education", orientation="h", text_auto=True)
    fig3 = apply_layout(fig3, title="Education Level")
    st.plotly_chart(fig3, use_container_width=True)

# Family Status + Income Type
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Family Status")
    if "NAME_FAMILY_STATUS" in filtered.columns:
        fam_cnt = filtered["NAME_FAMILY_STATUS"].value_counts().reset_index()
        fam_cnt.columns = ["Family Status", "Count"]
        fig4 = px.bar(fam_cnt, x="Family Status", y="Count", text_auto=True)
        fig4 = apply_layout(fig4, title="Family Status")
        st.plotly_chart(fig4, use_container_width=True)

with col_d:
    st.subheader("Income Type")
    if "NAME_INCOME_TYPE" in filtered.columns:
        inc_cnt = filtered["NAME_INCOME_TYPE"].value_counts().reset_index()
        inc_cnt.columns = ["Income Type", "Count"]
        fig5 = px.bar(inc_cnt, x="Count", y="Income Type", orientation="h", text_auto=True)
        fig5 = apply_layout(fig5, title="Income Type")
        st.plotly_chart(fig5, use_container_width=True)

# Age Group by Gender
if "AGE_GROUP" in filtered.columns and "CODE_GENDER" in filtered.columns:
    st.subheader("Age Group by Gender")
    age_gender = filtered.groupby(["AGE_GROUP", "CODE_GENDER"]).size().reset_index(name="Count")
    fig6 = px.bar(age_gender, x="AGE_GROUP", y="Count", color="CODE_GENDER", barmode="group", text_auto=True)
    fig6 = apply_layout(fig6, title="Age Group by Gender")
    st.plotly_chart(fig6, use_container_width=True)

# ===================== INSIGHTS =====================
st.subheader("Key Observations")
st.write(f"- Average customer age is **{avg_age:.1f}** years.")
st.write(f"- Most common gender: **{most_gender}**")
st.write(f"- Most common education: **{most_education}**")
st.write(f"- Most common income type: **{most_income_type}**")
st.write(f"- Most common family status: **{most_family}**")

st.subheader("Recommendations")
st.write("1. Understand the typical customer profile before designing products.")
st.write("2. Check if certain age groups or education levels have higher defaults (see later pages).")
st.write("3. Use demographic filters to explore different customer segments.")