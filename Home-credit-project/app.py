"""
Home Credit 20-Page Streamlit EDA & Preprocessing Dashboard
Main entry point.
"""

import streamlit as st

st.set_page_config(
    page_title="Home Credit Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏦 Home Credit Analytics Dashboard")
st.markdown("""
### 20-Page Exploratory Data Analysis & Preprocessing Project

This interactive dashboard covers the complete analytics lifecycle for the **Home Credit Default Risk** dataset:

1. **Data Understanding & Quality**
2. **Missing Value & Outlier Analysis**
3. **Feature Engineering**
4. **Customer Demographics, Income & Employment**
5. **Loan Affordability & Default Risk EDA**
6. **Bureau, Previous Applications, Installments & Credit Cards**
7. **Rule-based Risk Segmentation**
8. **Executive Insights & Business Recommendations**

---

**How to use**
- Use the **sidebar** to navigate between the 20 analytical pages.
- Apply filters on each page to explore specific customer segments.
- All analysis is descriptive – **no machine-learning models** are built.

---

**Datasets loaded**
- `application_train.csv` (main table with TARGET)
- `bureau.csv` & `bureau_balance`
- `previous_application.csv`
- `POS_CASH_balance`
- `installments_payments.csv`
- `credit_card_balance.csv`

Select a page from the sidebar to begin.
""")

st.info("➡️ Start with **01 Executive Overview** in the sidebar.")