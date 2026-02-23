import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")

    if st.session_state.get("last_date") != selected_date:
        st.session_state["last_date"] = selected_date
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        st.session_state["existing_expenses"] = response.json() if response.status_code == 200 else []

    existing_expenses = st.session_state.get("existing_expenses", [])

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # ✅ Form key changes with date — forces Streamlit to treat it as a brand new form
    form_key = f"expense_form_{selected_date}"

    with st.form(key=form_key):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=float(amount), key=f"amount_{i}_{selected_date}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category), key=f"category_{i}_{selected_date}", label_visibility="collapsed")
            with col3:
                note_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}_{selected_date}", label_visibility="collapsed")

            expenses.append({
                'amount' : amount_input,
                'category' :category_input,
                'notes' : note_input
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]
            
            post_response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)

            if post_response.status_code == 200:
                st.success("Expense updated Successfully")
            else:
                st.error("Failed to update expense")
                