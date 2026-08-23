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

st.set_page_config(page_title="Family & Housing", page_icon="🏦", layout="wide")
st.title("🏠 08 · Family & Housing Analysis ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

st.subheader("Family & Housing Metrics")
avg_fam = filtered["CNT_FAM_MEMBERS"].mean() if "CNT_FAM_MEMBERS" in filtered.columns else 0
avg_child = filtered["CNT_CHILDREN"].mean() if "CNT_CHILDREN" in filtered.columns else 0
c1, c2, c3 = st.columns(3)
c1.metric("Average Family Size", f"{avg_fam:.1f}")
c2.metric("Average Children", f"{avg_child:.1f}")
c3.metric("Customers", format_number(filtered["SK_ID_CURR"].nunique()))

st.divider()

col_a, col_b = st.columns(2)
with col_a:
    if "CNT_FAM_MEMBERS" in filtered.columns:
        st.subheader("Family Size Distribution")
        fig1 = px.histogram(filtered, x="CNT_FAM_MEMBERS", nbins=20)
        st.plotly_chart(apply_layout(fig1), use_container_width=True)

with col_b:
    if "CNT_CHILDREN" in filtered.columns:
        st.subheader("Number of Children")
        child = filtered["CNT_CHILDREN"].value_counts().reset_index()
        child.columns = ["Children", "Count"]
        fig2 = px.bar(child, x="Children", y="Count", text_auto=True)
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

if "NAME_HOUSING_TYPE" in filtered.columns:
    st.subheader("Housing Type")
    house = filtered["NAME_HOUSING_TYPE"].value_counts().reset_index()
    house.columns = ["Housing Type", "Count"]
    fig3 = px.bar(house, x="Housing Type", y="Count", text_auto=True)
    st.plotly_chart(apply_layout(fig3), use_container_width=True)

col_c, col_d = st.columns(2)
with col_c:
    if "FLAG_OWN_REALTY" in filtered.columns:
        st.subheader("Property Ownership")
        realty = filtered["FLAG_OWN_REALTY"].value_counts()
        fig4 = go.Figure(data=[go.Pie(labels=realty.index, values=realty.values, hole=0.4)])
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

with col_d:
    if "FLAG_OWN_CAR" in filtered.columns:
        st.subheader("Car Ownership")
        car = filtered["FLAG_OWN_CAR"].value_counts()
        fig5 = go.Figure(data=[go.Pie(labels=car.index, values=car.values, hole=0.4)])
        st.plotly_chart(apply_layout(fig5), use_container_width=True)

st.subheader("Key Observations")
st.write(f"- Average family size: **{avg_fam:.1f}**")
st.write(f"- Average number of children: **{avg_child:.1f}**")

st.subheader("Recommendations")
st.write("1. Larger families may have higher living costs.")
st.write("2. Check affordability for customers with many children.")