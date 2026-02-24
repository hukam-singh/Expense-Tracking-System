import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

CATEGORY_EMOJI = {
    "Rent": "🏠",
    "Food": "🍔",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Other": "📦",
}
CATEGORY_COLORS = {
    "Rent": "#f87171",
    "Food": "#34d399",
    "Shopping": "#60a5fa",
    "Entertainment": "#a78bfa",
    "Other": "#fbbf24",
}

def add_update_tab():
    st.markdown('<div class="section-title">Add / Update Expenses</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Enter up to 5 expenses for any date.</div>', unsafe_allow_html=True)

    col_date, col_info = st.columns([1, 2])
    with col_date:
        selected_date = st.date_input("Select Date", datetime(2024, 8, 1))

    # Fetch existing expenses when date changes
    if st.session_state.get("last_date") != selected_date:
        st.session_state["last_date"] = selected_date
        with st.spinner("Loading expenses…"):
            try:
                response = requests.get(f"{API_URL}/expenses/{selected_date}", timeout=5)
                st.session_state["existing_expenses"] = response.json() if response.status_code == 200 else []
            except Exception:
                st.session_state["existing_expenses"] = []

    existing_expenses = st.session_state.get("existing_expenses", [])
    categories = list(CATEGORY_EMOJI.keys())

    # Running total display
    total_existing = sum(e.get("amount", 0) for e in existing_expenses)
    with col_info:
        if existing_expenses:
            st.markdown(f"""
            <div style="margin-top:1.6rem; background:rgba(249,212,35,0.1); border:1px solid rgba(249,212,35,0.25);
                        border-radius:12px; padding:0.7rem 1.2rem; display:inline-block;">
                <span style="color:#a0a0c0; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px;">
                    Recorded for this date</span><br>
                <span style="font-family:'DM Serif Display',serif; font-size:1.5rem; color:#f9d423;">
                    ₹ {total_existing:,.2f}</span>
                <span style="color:#a0a0c0; font-size:0.78rem;"> · {len(existing_expenses)} entries</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    form_key = f"expense_form_{selected_date}"

    with st.form(key=form_key):
        # Column headers
        _, c1, c2, c3 = st.columns([0.3, 1, 1, 1.5])
        with c1: st.markdown('<div class="col-header">Amount (₹)</div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="col-header">Category</div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="col-header">Notes</div>', unsafe_allow_html=True)

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount   = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes    = existing_expenses[i]['notes']
            else:
                amount, category, notes = 0.0, "Shopping", ""

            badge_col, col1, col2, col3 = st.columns([0.3, 1, 1, 1.5])
            with badge_col:
                st.markdown(f'<div class="row-badge">{i+1}</div>', unsafe_allow_html=True)
            with col1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=1.0, value=float(amount),
                    key=f"amount_{i}_{selected_date}", label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category", options=categories,
                    index=categories.index(category) if category in categories else 0,
                    key=f"category_{i}_{selected_date}", label_visibility="collapsed",
                    format_func=lambda c: f"{CATEGORY_EMOJI.get(c,'')} {c}"
                )
            with col3:
                note_input = st.text_input(
                    label="Notes", value=notes,
                    key=f"notes_{i}_{selected_date}", label_visibility="collapsed",
                    placeholder="Optional note…"
                )
            expenses.append({'amount': amount_input, 'category': category_input, 'notes': note_input})

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Live total preview (computed from current widget values via session state isn't available mid-form,
        # so show a static note)
        st.markdown("""
        <div style="color:#a0a0c0; font-size:0.8rem; margin-bottom:0.5rem;">
            ℹ️ Rows with ₹0 amount will be ignored on save.
        </div>
        """, unsafe_allow_html=True)

        submit_button = st.form_submit_button("💾  Save Expenses")
        if submit_button:
            filtered_expenses = [e for e in expenses if e['amount'] > 0]
            if not filtered_expenses:
                st.warning("No expenses to save — all amounts are ₹0.")
            else:
                with st.spinner("Saving…"):
                    try:
                        post_response = requests.post(
                            f"{API_URL}/expenses/{selected_date}",
                            json=filtered_expenses, timeout=5
                        )
                        if post_response.status_code == 200:
                            total = sum(e['amount'] for e in filtered_expenses)
                            st.success(f"✅ Saved {len(filtered_expenses)} expense(s) · Total: ₹{total:,.2f}")
                            st.session_state["existing_expenses"] = filtered_expenses
                        else:
                            st.error("❌ Failed to save expenses. Check your API server.")
                    except Exception as ex:
                        st.error(f"❌ Connection error: {ex}")