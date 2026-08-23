import pandas as pd
from pathlib import Path
import numpy as np

DATA_PATH = Path(__file__).parent.parent / "data"


def _load_or_demo(filename, demo_dict):
	file = DATA_PATH / filename
	if file.exists():
		try:
			return pd.read_csv(file)
		except Exception:
			pass
	# Return demo data if file not found
	return pd.DataFrame(demo_dict)


def load_bureau_balance():
	return _load_or_demo("bureau_balance.csv", {
		'SK_ID_BUREAU': range(1, 1001),
		'MONTHS_BALANCE': np.random.randint(-48, 0, 1000),
		'STATUS': np.random.choice(['0', '1', '2', 'C', 'X'], 1000)
	})


def load_pos_cash_balance():
	return _load_or_demo("POS_CASH_balance.csv", {
		'SK_ID_PREV': range(1, 1001),
		'MONTHS_BALANCE': np.random.randint(-48, 0, 1000),
		'SK_DPD': np.random.randint(0, 30, 1000)
	})


def load_bureau():
	return _load_or_demo("bureau.csv", {
		'SK_ID_CURR': range(1, 1001),
		'CREDIT_DAY_OVERDUE': np.random.randint(0, 100, 1000)
	})


def load_credit_card_balance():
	return _load_or_demo("credit_card_balance.csv", {
		'SK_ID_PREV': range(1, 1001),
		'MONTHS_BALANCE': np.random.randint(-48, 0, 1000),
		'AMT_BALANCE': np.random.randint(0, 10000, 1000)
	})


def load_installments():
	return _load_or_demo("installments_payments.csv", {
		'SK_ID_PREV': range(1, 1001),
		'AMT_INSTALMENT': np.random.randint(1000, 10000, 1000)
	})


def load_previous():
	return _load_or_demo("previous_application.csv", {
		'SK_ID_PREV': range(1, 1001),
		'AMT_APPLICATION': np.random.randint(1000, 50000, 1000)
	})


# Add aliases so old page names still work
def load_pos_cash():
	return load_pos_cash_balance()


def load_bureau_balance_data():
	return load_bureau_balance()


def load_credit_card():
	return load_credit_card_balance()


def load_installments_payments():
	return load_installments()


def load_previous_application():
	return load_previous()
