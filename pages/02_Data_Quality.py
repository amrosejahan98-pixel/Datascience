import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_application
from utils.preprocessing import clean_application, get_data_quality_summary
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Data Quality", page_icon="🏦", layout="wide")
st.title("📋 02 · Data Quality Dashboard ")

# Load data
df = load_application()
df = clean_application(df)
filtered = apply_sidebar_filters(df)

# ===================== KPI CARDS =====================
st.subheader("Data Quality Metrics")

summary = get_data_quality_summary(filtered)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rows", format_number(summary["rows"]))
col2.metric("Total Columns", format_number(summary["columns"]))
col3.metric("Numeric Columns", format_number(summary["numeric_cols"]))
col4.metric("Categorical Columns", format_number(summary["categorical_cols"]))

col5, col6, col7, col8 = st.columns(4)
col5.metric("Missing Cells", format_number(summary["missing_cells"]))
col6.metric("Missing %", f"{summary['missing_pct']}%")
col7.metric("Duplicate Rows", format_number(summary["duplicate_rows"]))
col8.metric("Unique Customers", format_number(summary["unique_customers"]))

st.divider()

# ===================== COLUMN INFO TABLE =====================
st.subheader("Column Details")

info_data = []
for col in filtered.columns:
    info_data.append({
        "Column Name": col,
        "Data Type": str(filtered[col].dtype),
        "Missing Count": filtered[col].isnull().sum(),
        "Missing %": round(filtered[col].isnull().sum() / len(filtered) * 100, 2),
        "Unique Values": filtered[col].nunique()
    })

info_df = pd.DataFrame(info_data)
st.dataframe(info_df, use_container_width=True)

st.divider()

# ===================== CHARTS =====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Data Types Count")
    dtype_counts = filtered.dtypes.astype(str).value_counts().reset_index()
    dtype_counts.columns = ["Data Type", "Count"]
    fig1 = px.bar(dtype_counts, x="Data Type", y="Count", text_auto=True)
    fig1 = apply_layout(fig1, title="Column Data Types")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Top 10 Missing Columns")
    missing = info_df[info_df["Missing Count"] > 0].sort_values("Missing %", ascending=False).head(10)
    if len(missing) > 0:
        fig2 = px.bar(missing, x="Missing %", y="Column Name", orientation="h", text_auto=True)
        fig2 = apply_layout(fig2, title="Top Missing Columns")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.success("No missing values found!")

# ===================== INSIGHTS =====================
st.subheader("Key Observations")
st.write(f"- Dataset has **{format_number(summary['rows'])}** rows and **{summary['columns']}** columns.")
st.write(f"- Total missing cells: **{format_number(summary['missing_cells'])}** ({summary['missing_pct']}%)")
st.write(f"- Duplicate rows: **{summary['duplicate_rows']}**")
st.write(f"- Unique customers: **{format_number(summary['unique_customers'])}**")

st.subheader("Recommendations")
st.write("1. Investigate columns with high missing percentage.")
st.write("2. Check data types of important columns.")
st.write("3. Remove or treat duplicate rows if any.")