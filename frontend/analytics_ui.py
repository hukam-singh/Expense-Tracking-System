import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

CATEGORY_COLORS = {
    "Rent":          "#f87171",
    "Food":          "#34d399",
    "Shopping":      "#60a5fa",
    "Entertainment": "#a78bfa",
    "Other":         "#fbbf24",
}

def analytics_tab():
    st.markdown('<div class="section-title">Analytics by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Visualise your spending breakdown over any date range.</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 0.6])
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        fetch = st.button("🔍  Get Analytics")

    if fetch:
        if start_date > end_date:
            st.error("Start date must be before end date.")
            return

        with st.spinner("Fetching analytics…"):
            try:
                payload = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date":   end_date.strftime("%Y-%m-%d"),
                }
                response = requests.post(f"{API_URL}/analytics/", json=payload, timeout=5)
                data_raw = response.json()
            except Exception as ex:
                st.error(f"❌ Connection error: {ex}")
                return

        if not data_raw:
            st.info("No expense data found for this date range.")
            return

        df = pd.DataFrame({
            "Category":   list(data_raw.keys()),
            "Total":      [data_raw[c]["total"]      for c in data_raw],
            "Percentage": [data_raw[c]["percentage"] for c in data_raw],
        }).sort_values("Percentage", ascending=False).reset_index(drop=True)

        total_spend = df["Total"].sum()

        # ── KPI strip ──────────────────────────────────────────────────────
        top_cat = df.iloc[0]["Category"]
        top_pct = df.iloc[0]["Percentage"]
        days = (end_date - start_date).days + 1

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="label">Total Spent</div>
                <div class="value">₹{total_spend:,.0f}</div>
                <div class="sub">{days} day{'s' if days>1 else ''}</div>
            </div>
            <div class="metric-card">
                <div class="label">Daily Average</div>
                <div class="value">₹{total_spend/days:,.0f}</div>
                <div class="sub">per day</div>
            </div>
            <div class="metric-card">
                <div class="label">Top Category</div>
                <div class="value" style="font-size:1.4rem;">{top_cat}</div>
                <div class="sub">{top_pct:.1f}% of spend</div>
            </div>
            <div class="metric-card">
                <div class="label">Categories</div>
                <div class="value">{len(df)}</div>
                <div class="sub">active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Charts side-by-side ─────────────────────────────────────────────
        chart_col1, chart_col2 = st.columns(2)

        colors = [CATEGORY_COLORS.get(c, "#94a3b8") for c in df["Category"]]

        with chart_col1:
            st.markdown('<div style="color:#a0a0c0;font-size:0.8rem;text-transform:uppercase;'
                        'letter-spacing:1px;margin-bottom:0.5rem;">Spend Share (%)</div>',
                        unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                x=df["Category"], y=df["Percentage"],
                marker_color=colors,
                marker_line_width=0,
                text=df["Percentage"].map("{:.1f}%".format),
                textposition="outside",
                textfont=dict(color="#d0d0e0", size=11),
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#a0a0c0", family="DM Sans"),
                xaxis=dict(showgrid=False, color="#a0a0c0"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", color="#a0a0c0",
                           ticksuffix="%"),
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            st.markdown('<div style="color:#a0a0c0;font-size:0.8rem;text-transform:uppercase;'
                        'letter-spacing:1px;margin-bottom:0.5rem;">Composition (Donut)</div>',
                        unsafe_allow_html=True)
            fig_pie = go.Figure(go.Pie(
                labels=df["Category"], values=df["Total"],
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#1a1a3e", width=3)),
                textinfo="percent",
                textfont=dict(color="#1a1a2e", size=11),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#a0a0c0", family="DM Sans"),
                showlegend=True,
                legend=dict(orientation="v", font=dict(color="#d0d0e0", size=11),
                            bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # ── Summary table ───────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="color:#a0a0c0;font-size:0.8rem;text-transform:uppercase;'
                    'letter-spacing:1px;margin-bottom:0.8rem;">Breakdown Table</div>',
                    unsafe_allow_html=True)

        df_display = df.copy()
        df_display["Total"]      = df_display["Total"].map("₹ {:,.2f}".format)
        df_display["Percentage"] = df_display["Percentage"].map("{:.2f} %".format)
        df_display.index = range(1, len(df_display) + 1)
        st.table(df_display)