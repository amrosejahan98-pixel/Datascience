import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_bureau_balance
from utils.metrics import format_number
from utils.charts import apply_layout

st.set_page_config(page_title="Bureau Balance Analysis", page_icon="📊")
st.title("📊 14 · Bureau Balance Analysis")



df = load_bureau_balance()

if df is None:
	st.warning("⚠️ `bureau_balance.csv` not found - showing demo data so app doesn't crash")
	import numpy as np
	df = pd.DataFrame({
		'SK_ID_BUREAU': range(1, 1001),
		'MONTHS_BALANCE': np.random.randint(-48, 0, 1000),
		'STATUS': np.random.choice(['0','1','2','C','X'], 1000)
	})
	st.info("Add real `bureau_balance.csv` to `data/` folder for full analysis")

st.write(f"### Bureau Balance Data: {len(df):,} records")
st.dataframe(df.head())

fig = px.histogram(df, x="STATUS", title="Bureau Balance Status Distribution")
st.plotly_chart(fig, use_container_width=True)

fig2 = px.histogram(df, x="MONTHS_BALANCE", title="Months Balance Trend")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Bureau Balance Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Total Records", format_number(len(df)))
c2.metric("Unique Bureau IDs", format_number(df['SK_ID_BUREAU'].nunique()))
c3.metric("Avg Months Balance", f"{df['MONTHS_BALANCE'].mean():.1f}")
