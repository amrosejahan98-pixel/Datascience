import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_pos_cash_balance
from utils.metrics import format_number


st.title("16 · POS CASH Analysis")
pos = load_pos_cash_balance()

st.metric("Total Records", format_number(len(pos)))
st.dataframe(pos.head())
fig = px.histogram(pos, x="MONTHS_BALANCE", title="POS CASH Balance")
st.plotly_chart(fig, use_container_width=True)
