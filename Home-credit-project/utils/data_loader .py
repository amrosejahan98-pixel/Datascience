import pandas as pd
from pathlib import Path

def _load(name, demo):
    p = Path(__file__).parent.parent / "data" / name
    try:
        return pd.read_csv(p)
    except:
        return pd.DataFrame(demo)

def load_application():
    return _load('application_train.csv', {'SK_ID_CURR': range(1,1001), 'TARGET': [0,1]*500})

def load_bureau(): return _load('bureau.csv', {'SK_ID_CURR': range(1,1001)})
def load_bureau_balance(): return _load('bureau_balance.csv', {'SK_ID_BUREAU': range(1,1001)})
def load_pos_cash_balance(): return _load('POS_CASH_balance.csv', {'SK_ID_PREV': range(1,1001)})
def load_credit_card_balance(): return _load('credit_card_balance.csv', {'SK_ID_PREV': range(1,1001)})
def load_installments(): return _load('installments_payments.csv', {'SK_ID_PREV': range(1,1001)})
def load_previous(): return _load('previous_application.csv', {'SK_ID_PREV': range(1,1001)})
def load_application_train(): return load_application()
def load_app(): return load_application()
def load_pos_cash(): return load_pos_cash_balance()