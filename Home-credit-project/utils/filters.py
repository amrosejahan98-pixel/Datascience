import streamlit as st

def apply_sidebar_filters(df):
    st.sidebar.header("Filters")
    
    filtered = df.copy()
    
    # Gender filter
    if "CODE_GENDER" in filtered.columns:
        gender = st.sidebar.multiselect(
            "Gender",
            options=filtered["CODE_GENDER"].unique(),
            default=filtered["CODE_GENDER"].unique()
        )
        filtered = filtered[filtered["CODE_GENDER"].isin(gender)]
    
    # Contract Type filter
    if "NAME_CONTRACT_TYPE" in filtered.columns:
        contract = st.sidebar.multiselect(
            "Contract Type",
            options=filtered["NAME_CONTRACT_TYPE"].unique(),
            default=filtered["NAME_CONTRACT_TYPE"].unique()
        )
        filtered = filtered[filtered["NAME_CONTRACT_TYPE"].isin(contract)]
    
    return filtered