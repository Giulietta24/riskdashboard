import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Portfolio Risk Dashboard", layout="wide")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

st.title("Portfolio Risk Dashboard")
st.caption("Broker-style portfolio review with holdings, options, and risk focus.")

uploaded = st.sidebar.file_uploader("Upload portfolio CSV", type=["csv"])

sample = pd.DataFrame([
    {"section": "Long Stocks", "ticker": "SOFI", "qty": 600, "avg_price": 28.31, "last": 18.47, "market_value": 11082.0, "delta": 600, "theta": 0, "vega": 0, "unrealized_pnl": -5892.0},
    {"section": "Long Stocks", "ticker": "GRAB", "qty": 600, "avg_price": 5.60, "last": 3.46, "market_value": 2076.0, "delta": 600, "theta": 0, "vega": 0, "unrealized_pnl": -1284.0},
    {"section": "Long Stocks", "ticker": "SBET", "qty": 500, "avg_price": 19.86, "last": 5.63, "market_value": 2815.0, "delta": 500, "theta": 0, "vega": 0, "unrealized_pnl": -7115.0},
    {"section": "Options", "ticker": "RKLB 85P", "qty": -5, "avg_price": 5.792, "last": 6.50, "market_value": -2331.0, "delta": -0.195, "theta": -0.093, "vega": 0.124, "unrealized_pnl": -163.0},
    {"section": "Options", "ticker": "SOFI 28C", "qty": -5, "avg_price": 0.452, "last": 0.58, "market_value": -239.0, "delta": 0.192, "theta": -0.008, "vega": 0.029, "unrealized_pnl": -70.0},
    {"section": "Options", "ticker": "NVDA 180P", "qty": -1, "avg_price": 1.103, "last": 1.22, "market_value": -88.0, "delta": -0.097, "theta": 0.007, "vega": 0.111, "unrealized_pnl": -6.0},
])

df = pd.read_csv(uploaded) if uploaded is not None else sample.copy()

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Positions", "Risk", "History"])

with tab1:
    st.subheader("Account Snapshot")

    total_mv = float(df["market_value"].sum()) if "market_value" in df.columns else 0.0
    total_pnl = float(df["unrealized_pnl"].sum()) if "unrealized_pnl" in df.columns else 0.0
    total_delta = float(df["delta"].sum()) if "delta" in df.columns else 0.0
    total_theta = float(df["theta"].sum()) if "theta" in df.columns else 0.0
    total_vega = float(df["vega"].sum()) if "vega" in df.columns else 0.0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Net Liquidity", "$48.7K", None)
    c2.metric("Market Value", f"${total_mv:,.0f}")
    c3.metric("Unrealized P&L", f"${total_pnl:,.0f}")
    c4.metric("Theta", f"{total_theta:,.2f}")
    c5.metric("Vega", f"{total_vega:,.2f}")

    if "section" in df.columns:
        section_mv = df.groupby("section", as_index=False)["market_value"].sum()
        fig = px.pie(section_mv, names="section", values="market_value", title="Exposure by Section")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Positions")
    st.dataframe(df, use_container_width=True)

    if "ticker" in df.columns and "market_value" in df.columns:
        by_ticker = df.groupby("ticker", as_index=False)["market_value"].sum().sort_values("market_value", ascending=False)
        fig = px.bar(by_ticker, x="ticker", y="market_value", title="Market Value by Ticker")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Risk Review")

    risk_cols = [c for c in ["ticker", "section", "qty", "delta", "theta", "vega", "unrealized_pnl"] if c in df.columns]
    if risk_cols:
        st.dataframe(df[risk_cols], use_container_width=True)

    st.markdown(
        """
- Focus first on concentrated short-option exposure.
- Watch names with both stock and option exposure.
- Add stress tests for +/-5% and +/-10% price moves.
- Add a summary of short puts, short calls, and defined-risk spreads.
"""
    )

    if {"ticker", "unrealized_pnl"}.issubset(df.columns):
        stress = df.copy()
        stress["stress_down_5"] = np.where(stress["qty"] > 0, stress["unrealized_pnl"] * 1.5, stress["unrealized_pnl"] * 1.8)
        stress["stress_up_5"] = np.where(stress["qty"] > 0, stress["unrealized_pnl"] * 0.8, stress["unrealized_pnl"] * 1.2)
        st.dataframe(stress[["ticker", "unrealized_pnl", "stress_down_5", "stress_up_5"]], use_container_width=True)

with tab4:
    st.subheader("History")

    history_file = DATA_DIR / "snapshots.csv"
    snapshot = df.copy()
    snapshot["timestamp"] = datetime.now().isoformat(timespec="seconds")

    if st.button("Save snapshot"):
        if history_file.exists():
            old = pd.read_csv(history_file)
            out = pd.concat([old, snapshot], ignore_index=True)
        else:
            out = snapshot
        out.to_csv(history_file, index=False)
        st.success("Snapshot saved.")

    if history_file.exists():
        hist = pd.read_csv(history_file)
        st.dataframe(hist, use_container_width=True)

        if {"timestamp", "unrealized_pnl"}.issubset(hist.columns):
            if "timestamp" in hist.columns:
                grp = hist.groupby("timestamp", as_index=False)["unrealized_pnl"].sum()
                fig = px.line(grp, x="timestamp", y="unrealized_pnl", title="Unrealized P&L Over Time")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No saved history yet.")
