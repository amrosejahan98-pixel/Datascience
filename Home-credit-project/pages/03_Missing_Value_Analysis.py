import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_application
from utils.preprocessing import clean_application
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Missing Value Analysis", page_icon="🏦", layout="wide")
st.title("🔍 03 · Missing Value Analysis ")

# Load data
df = load_application()
df = clean_application(df)
filtered = apply_sidebar_filters(df)

# ===================== KPI CARDS =====================
st.subheader("Missing Value Metrics")

total_missing = filtered.isnull().sum().sum()
total_cells = filtered.shape[0] * filtered.shape[1]
missing_pct = round(total_missing / total_cells * 100, 2)
cols_with_missing = (filtered.isnull().sum() > 0).sum()
cols_above_30 = (filtered.isnull().sum() / len(filtered) * 100 > 30).sum()
cols_above_50 = (filtered.isnull().sum() / len(filtered) * 100 > 50).sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Missing Values", format_number(total_missing))
col2.metric("Missing Percentage", f"{missing_pct}%")
col3.metric("Columns with Missing", format_number(cols_with_missing))
col4.metric("Columns > 30% Missing", format_number(cols_above_30))
col5.metric("Columns > 50% Missing", format_number(cols_above_50))

st.divider()

# ===================== MISSING TABLE =====================
st.subheader("Missing Values by Column")

miss_df = pd.DataFrame({
    "Column": filtered.columns,
    "Missing Count": filtered.isnull().sum().values,
    "Missing %": (filtered.isnull().sum().values / len(filtered) * 100).round(2)
})
miss_df = miss_df[miss_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)

st.dataframe(miss_df, use_container_width=True)

st.divider()

# ===================== CHARTS =====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Top 15 Columns by Missing %")
    top_miss = miss_df.head(15)
    if len(top_miss) > 0:
        fig1 = px.bar(top_miss, x="Missing %", y="Column", orientation="h", text_auto=True)
        fig1 = apply_layout(fig1, title="Top Missing Columns")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.success("No missing values!")

with col_b:
    st.subheader("Missing % Distribution")
    if len(miss_df) > 0:
        fig2 = px.histogram(miss_df, x="Missing %", nbins=20)
        fig2 = apply_layout(fig2, title="Distribution of Missing Percentage")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.success("No missing values!")

# ===================== CATEGORIES =====================
st.subheader("Missing Value Categories")

def missing_category(pct):
    if pct <= 5:
        return "0-5%"
    elif pct <= 20:
        return "5-20%"
    elif pct <= 40:
        return "20-40%"
    elif pct <= 60:
        return "40-60%"
    else:
        return "60%+"

if len(miss_df) > 0:
    miss_df["Category"] = miss_df["Missing %"].apply(missing_category)
    cat_counts = miss_df["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    
    fig3 = px.bar(cat_counts, x="Category", y="Count", text_auto=True)
    fig3 = apply_layout(fig3, title="Columns by Missing Category")
    st.plotly_chart(fig3, use_container_width=True)

# ===================== INSIGHTS =====================
st.subheader("Key Observations")
st.write(f"- Total missing values: **{format_number(total_missing)}** ({missing_pct}%)")
st.write(f"- Columns with missing data: **{cols_with_missing}**")
st.write(f"- Columns with more than 30% missing: **{cols_above_30}**")
st.write(f"- Columns with more than 50% missing: **{cols_above_50}**")

st.subheader("Recommendations")
st.write("1. Drop columns with more than 60% missing if not important.")
st.write("2. Fill numeric columns with median.")
st.write("3. Fill categorical columns with mode.")
st.write("4. Keep missing indicator for important columns.")