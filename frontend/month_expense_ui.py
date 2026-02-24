import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

MONTH_COLORS = [
    "#f9d423","#ff4e50","#34d399","#60a5fa","#a78bfa","#fbbf24",
    "#f87171","#6ee7b7","#93c5fd","#c4b5fd","#fcd34d","#fb7185",
]

def analytics_by_month():
    st.markdown('<div class="section-title">Analytics by Month</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">See how your spending trends across the year.</div>',
                unsafe_allow_html=True)

    col_btn, _ = st.columns([0.35, 0.65])
    with col_btn:
        fetch = st.button("📅  Get Monthly Analytics")

    if fetch:
        with st.spinner("Fetching monthly data…"):
            try:
                # fixed the space-in-URL bug: endpoint should be /expense-by-month/
                response = requests.get(f"{API_URL}/expense%20by%20month/", timeout=5)
                data_raw = response.json()
            except Exception as ex:
                st.error(f"❌ Connection error: {ex}")
                return

        if not data_raw:
            st.info("No monthly data available.")
            return

        # Backend returns a list of dicts: [{month_num, month, total_expense}, ...]
        if isinstance(data_raw, list):
            df = pd.DataFrame({
                "S.No":  [e["month_num"]     for e in data_raw],
                "Month": [e["month"]         for e in data_raw],
                "Total": [e["total_expense"] for e in data_raw],
            })
        elif isinstance(data_raw, dict):
            rows = []
            for i, (key, val) in enumerate(data_raw.items(), start=1):
                if isinstance(val, dict):
                    rows.append({
                        "S.No":  val.get("month_num", i),
                        "Month": val.get("month", key),
                        "Total": val.get("total_expense", val.get("total", 0)),
                    })
                else:
                    rows.append({"S.No": i, "Month": key, "Total": val})
            df = pd.DataFrame(rows)
        else:
            st.error("Unexpected data format from API.")
            st.json(data_raw)
            return

        df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)

        total_year  = df["Total"].sum()
        peak_row    = df.loc[df["Total"].idxmax()]
        low_row     = df.loc[df["Total"].idxmin()]
        avg_monthly = total_year / len(df) if len(df) else 0

        # ── KPI strip ──────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="label">Annual Total</div>
                <div class="value">₹{total_year:,.0f}</div>
                <div class="sub">{len(df)} months tracked</div>
            </div>
            <div class="metric-card">
                <div class="label">Monthly Avg</div>
                <div class="value">₹{avg_monthly:,.0f}</div>
                <div class="sub">per month</div>
            </div>
            <div class="metric-card">
                <div class="label">Peak Month</div>
                <div class="value" style="font-size:1.4rem;">{peak_row['Month']}</div>
                <div class="sub">₹{peak_row['Total']:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="label">Lowest Month</div>
                <div class="value" style="font-size:1.4rem;">{low_row['Month']}</div>
                <div class="sub">₹{low_row['Total']:,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Bar chart ──────────────────────────────────────────────────────
        bar_colors = [MONTH_COLORS[i % len(MONTH_COLORS)] for i in range(len(df))]
        avg_line = [avg_monthly] * len(df)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["Month"], y=df["Total"],
            marker_color=bar_colors,
            marker_line_width=0,
            name="Monthly Spend",
            text=df["Total"].map("₹{:,.0f}".format),
            textposition="outside",
            textfont=dict(color="#d0d0e0", size=10),
            hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df["Month"], y=avg_line,
            mode="lines",
            name="Monthly Avg",
            line=dict(color="rgba(249,212,35,0.6)", width=2, dash="dot"),
            hoverinfo="skip",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a0a0c0", family="DM Sans"),
            xaxis=dict(showgrid=False, color="#a0a0c0"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                       color="#a0a0c0", tickprefix="₹"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#d0d0e0")),
            margin=dict(l=10, r=10, t=30, b=10),
            height=380,
            bargap=0.3,
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Trend line chart ───────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="color:#a0a0c0;font-size:0.8rem;text-transform:uppercase;'
                    'letter-spacing:1px;margin-bottom:0.6rem;">Spend Trend</div>',
                    unsafe_allow_html=True)

        fig2 = go.Figure(go.Scatter(
            x=df["Month"], y=df["Total"],
            mode="lines+markers",
            line=dict(color="#f9d423", width=2.5),
            marker=dict(color="#ff4e50", size=8, line=dict(color="#f9d423", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(249,212,35,0.07)",
            hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a0a0c0", family="DM Sans"),
            xaxis=dict(showgrid=False, color="#a0a0c0"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                       color="#a0a0c0", tickprefix="₹"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
        )
        st.plotly_chart(fig2, use_container_width=True)

        # ── Table ──────────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        df_display = df.copy()
        df_display["Total"] = df_display["Total"].map("₹ {:,.2f}".format)
        df_display = df_display.rename(columns={"S.No": "#", "Month": "Month", "Total": "Total Spent"})
        df_display = df_display.set_index("#")
        st.table(df_display)