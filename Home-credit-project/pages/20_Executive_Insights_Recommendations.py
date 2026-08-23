import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from pathlib import Path
def load_application():
    p = Path(__file__).parent.parent / "data" / "application_train.csv"
    if p.exists():
        try:
            return pd.read_csv(p)
        except:
            pass
    return pd.DataFrame({'SK_ID_CURR': range(1,1001), 'TARGET': [0,1]*500, 'RISK_SEGMENT': ['Low']*1000})
from utils.preprocessing import clean_application
from utils.feature_engineering import create_core_features
from utils.filters import apply_sidebar_filters
from utils.metrics import format_number, format_percent

st.set_page_config(page_title="Executive Insights", page_icon="🏦", layout="wide")
st.title("🎯 20 · Executive Insights & Recommendations ")

df = load_application()
df = clean_application(df)
df = create_core_features(df)
filtered = apply_sidebar_filters(df)

total_customers = filtered["SK_ID_CURR"].nunique()
default_rate = filtered["TARGET"].mean()
total_credit = filtered["AMT_CREDIT"].sum()
avg_credit = filtered["AMT_CREDIT"].mean()
avg_income = filtered["AMT_INCOME_TOTAL"].mean()

st.subheader("Executive KPIs")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Customers", format_number(total_customers))
c2.metric("Default Rate", format_percent(default_rate))
c3.metric("Total Credit Exposure", format_number(total_credit))
c4.metric("Average Credit", format_number(avg_credit))
c5.metric("Average Income", format_number(avg_income))

st.divider()

st.subheader("Top Portfolio Insights")
st.markdown("""
1. Overall default rate is relatively low, but some segments show higher observed risk.
2. Customers with higher Credit-to-Income ratios tend to show more repayment pressure.
3. Employment stability and income level are useful descriptive risk indicators.
4. Education and income type groups show different default patterns.
5. Previous application history and refusals provide useful behavioural context.
6. Late installment payments are one of the strongest observed risk signals.
7. High credit-card utilization can indicate financial stress.
8. Bureau data helps identify customers with many external active loans.
9. Younger customers and some occupation groups may need closer monitoring.
10. Affordability ratios should be part of regular portfolio review.
""")

st.subheader("Business Recommendations")
st.markdown("""
### Affordability
1. Review customers with extreme Credit-to-Income ratios.
2. Monitor customers with high Annuity-to-Income burden.

### Repayment Behaviour
3. Create early-warning reports for repeated late payments.
4. Track customers whose payment delays are increasing.

### Bureau & External Credit
5. Review customers with multiple active external loans.
6. Identify customers with significant overdue bureau balances.

### Credit Cards
7. Monitor customers consistently using a large share of their credit limit.

### Employment & Demographics
8. Include employment stability in manual review dashboards.
9. Review products and limits for higher-risk demographic segments.

### Data Quality
10. Improve collection of high-missing-value fields that matter for risk.
11. Standardize occupation and organization type values.

### Portfolio Monitoring
12. Build monthly risk-segment movement reports.
13. Track concentration of credit exposure in elevated-risk groups.
14. Use filters on every dashboard page for segmented review.
15. Keep this dashboard as an EDA and monitoring tool (not a scoring model).
""")

st.success("End of 20-page Home Credit EDA Dashboard.")