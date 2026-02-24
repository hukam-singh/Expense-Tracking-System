import streamlit as st

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1a1a2e;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Hero header ── */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    background: linear-gradient(90deg, #f9d423, #ff4e50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.hero-header p {
    color: #a0a0c0;
    font-size: 1rem;
    margin-top: 0.3rem;
    font-weight: 300;
}

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0;
}
.metric-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.2rem 2rem;
    min-width: 180px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(249,212,35,0.15);
}
.metric-card .label {
    color: #a0a0c0;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}
.metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #f9d423;
    margin-top: 0.2rem;
}
.metric-card .sub {
    font-size: 0.75rem;
    color: #ff4e50;
    margin-top: 0.15rem;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    color: #a0a0c0 !important;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.55rem 1.4rem;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #f9d423, #ff4e50) !important;
    color: #1a1a2e !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem;
}

/* ── Section titles ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.section-sub {
    color: #a0a0c0;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.2rem 0;
}

/* ── Cards / containers ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.8rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.2rem;
}

/* ── Input & select overrides ── */
.stNumberInput input, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.9rem;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #f9d423 !important;
    box-shadow: 0 0 0 2px rgba(249,212,35,0.2) !important;
}

/* ── Date input ── */
.stDateInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #f9d423, #ff4e50);
    color: #1a1a2e;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.8rem;
    font-size: 0.9rem;
    transition: opacity 0.2s, transform 0.15s;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255,78,80,0.3);
}
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #f9d423, #ff4e50) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2.5rem !important;
    font-size: 0.95rem !important;
    width: 100%;
    margin-top: 0.8rem;
}

/* ── Alerts ── */
.stSuccess { background: rgba(52,211,153,0.15) !important; border-color: #34d399 !important; color: #34d399 !important; border-radius: 10px !important; }
.stError   { background: rgba(248,113,113,0.15) !important; border-color: #f87171 !important; color: #f87171 !important; border-radius: 10px !important; }

/* ── Table ── */
.stTable table { background: transparent !important; }
.stTable th {
    background: rgba(249,212,35,0.15) !important;
    color: #f9d423 !important;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stTable td { color: #d0d0e0 !important; font-size: 0.9rem; }
.stTable tr:hover td { background: rgba(255,255,255,0.04) !important; }

/* ── Bar chart ── */
.stBarChart { border-radius: 12px; overflow: hidden; }

/* ── Column headers ── */
.col-header {
    color: #a0a0c0;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    padding-bottom: 4px;
}

/* ── Row number badge ── */
.row-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: rgba(249,212,35,0.18);
    border-radius: 6px;
    color: #f9d423;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 8px;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #f9d423 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(249,212,35,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from month_expense_ui import analytics_by_month

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>💸 Expense Tracker</h1>
    <p>Track • Analyze • Save Smarter</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["✏️  Add / Update", "📊  Analytics by Category", "📅  Analytics by Month"])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_by_month()