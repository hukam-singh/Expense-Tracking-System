import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from month_expense_ui import analytics_by_month


st.title("Expese Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analystics By Category", "Analystics By Month"])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_by_month()
