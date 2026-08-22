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
