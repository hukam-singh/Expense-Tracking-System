import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_by_month():
    if st.button("Get Analystics by Month"):
        st.title("Expense Breakdown by Month")
        response = requests.get(f"{API_URL}/expense by month/")
        response = response.json()

        data = {
            "S.no" : [expense["month_num"] for expense in response],
            "Month" : [expense["month"] for expense in response],
            "Total" : [expense["total_expense"] for expense in response]
        }


        df = pd.DataFrame(data)
            
        st.bar_chart(data=df.set_index("Month")['Total'])

        st.table(df.set_index("S.no"))