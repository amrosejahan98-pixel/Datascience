import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from pathlib import Path
def load_application():
    p = Path(__file__).parent.parent / "data" / "application_train.csv"
    try:
        return pd.read_csv(p)
    except:
        return pd.DataFrame({
            'SK_ID_CURR': range(1,1001),
            'TARGET': [0,1]*500,
            'RISK_SEGMENT': ['Low','Medium','High']*333 + ['Low'],
            'AMT_INCOME_TOTAL': [50000]*1000
        })
from utils.preprocessing import clean_application
from utils.feature_engineering import create_core_features
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Customer Risk Segmentation", page_icon="🏦", layout="wide")
st.title("🧩 19 · Customer Risk Segmentation ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

# Simple rule-based segmentation (EDA only, not prediction)
def risk_segment(row):
    score = 0
    if "CREDIT_TO_INCOME" in row and pd.notna(row["CREDIT_TO_INCOME"]):
        if row["CREDIT_TO_INCOME"] > 6:
            score += 2
        elif row["CREDIT_TO_INCOME"] > 3:
            score += 1
    if "ANNUITY_TO_INCOME" in row and pd.notna(row["ANNUITY_TO_INCOME"]):
        if row["ANNUITY_TO_INCOME"] > 0.3:
            score += 2
        elif row["ANNUITY_TO_INCOME"] > 0.2:
            score += 1
    if "TARGET" in row and row["TARGET"] == 1:
        score += 2
    if score >= 4:
        return "High Observed Risk"
    elif score >= 2:
        return "Elevated Observed Risk"
    elif score >= 1:
        return "Moderate Observed Risk"
    else:
        return "Low Observed Risk"

filtered = filtered.copy()
filtered["RISK_SEGMENT"] = filtered.apply(risk_segment, axis=1)

st.subheader("Risk Segment Metrics")
seg_counts = filtered["RISK_SEGMENT"].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Low Risk", format_number(seg_counts.get("Low Observed Risk", 0)))
c2.metric("Moderate Risk", format_number(seg_counts.get("Moderate Observed Risk", 0)))
c3.metric("Elevated Risk", format_number(seg_counts.get("Elevated Observed Risk", 0)))
c4.metric("High Risk", format_number(seg_counts.get("High Observed Risk", 0)))

st.divider()

st.subheader("Customer Count by Risk Segment")
seg_df = seg_counts.reset_index()
seg_df.columns = ["Risk Segment", "Count"]
fig1 = px.bar(seg_df, x="Risk Segment", y="Count", text_auto=True)
st.plotly_chart(apply_layout(fig1), use_container_width=True)

st.subheader("Portfolio Exposure by Segment")
exp = filtered.groupby("RISK_SEGMENT")["AMT_CREDIT"].sum().reset_index()
fig2 = px.pie(exp, names="RISK_SEGMENT", values="AMT_CREDIT", hole=0.4)
st.plotly_chart(apply_layout(fig2), use_container_width=True)

st.subheader("Average Income by Segment")
inc = filtered.groupby("RISK_SEGMENT")["AMT_INCOME_TOTAL"].mean().reset_index()
fig3 = px.bar(inc, x="RISK_SEGMENT", y="AMT_INCOME_TOTAL", text_auto=True)
st.plotly_chart(apply_layout(fig3), use_container_width=True)

st.subheader("How segments were created")
st.write("""
These are **descriptive EDA segments**, not model predictions.

Example rules used:
- High Credit-to-Income ratio
- High Annuity-to-Income ratio
- Already observed default (TARGET = 1)
""")

st.subheader("Recommendations")
st.write("1. Review High Observed Risk customers manually.")
st.write("2. Monitor Elevated Risk segment every month.")
st.write("3. Do not treat these segments as final credit decisions.")