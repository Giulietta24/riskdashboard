import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Theta Income Portfolio", layout="wide")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

st.title("Theta Income Portfolio")
st.caption("A broker-style dashboard for income-focused options portfolios.")

sample = pd.DataFrame([
    {"section": "Long Stocks", "ticker": "SOFI", "underlying": "SOFI", "instrument": "stock", "side": "long", "qty": 600, "avg_price": 28.31, "last": 18.47, "market_value": 11082.0, "delta": 600, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "unrealized_pnl": -5892.0, "expiry": "", "strike": np.nan},
    {"section": "Long Stocks", "ticker": "GRAB", "underlying": "GRAB", "instrument": "stock", "side": "long", "qty": 600, "avg_price": 5.60, "last": 3.46, "market_value": 2076.0, "delta": 600, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "unrealized_pnl": -1284.0, "expiry": "", "strike": np.nan},
    {"section": "Long Stocks", "ticker": "SBET", "underlying": "SBET", "instrument": "stock", "side": "long", "qty": 500, "avg_price": 19.86, "last": 5.63, "market_value": 2815.0, "delta": 500, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "unrealized_pnl": -7115.0, "expiry": "", "strike": np.nan},
    {"section": "Options", "ticker": "RKLB Jan'26 85P", "underlying": "RKLB", "instrument": "put", "side": "short", "qty": -5, "avg_price": 5.792, "last": 6.50, "market_value": -2331.0, "delta": -0.195, "gamma": 0.006, "theta": -0.093, "vega": 0.124, "unrealized_pnl": -163.0, "expiry": "2026-01-16", "strike": 85},
    {"section": "Options", "ticker": "MSTR Jul'26 65P", "underlying": "MSTR", "instrument": "put", "side": "short", "qty": -1, "avg_price": 1.258, "last": 0.30, "market_value": -24.0, "delta": -0.018, "gamma": 0.016, "theta": -0.032, "vega": 0.016, "unrealized_pnl": -70.0, "expiry": "2026-07-17", "strike": 65},
    {"section": "Options", "ticker": "SOFI Oct'26 28C", "underlying": "SOFI", "instrument": "call", "side": "short", "qty": -5, "avg_price": 0.452, "last": 0.58, "market_value": -239.0, "delta": 0.192, "gamma": 0.029, "theta": -0.008, "vega": 0.029, "unrealized_pnl": -70.0, "expiry": "2026-10-16", "strike": 28},
    {"section": "Options", "ticker": "ZETA Jul'26 33C", "underlying": "ZETA", "instrument": "call", "side": "short", "qty": -1, "avg_price": 0.128, "last": 0.03, "market_value": -25.0, "delta": 0.034, "gamma": 0.005, "theta": -0.006, "vega": 0.005, "unrealized_pnl": -22.0, "expiry": "2026-07-24", "strike": 33},
    {"section": "Options", "ticker": "GRAB Oct'26 5C", "underlying": "GRAB", "instrument": "call", "side": "short", "qty": -15, "avg_price": 0.205, "last": 0.46, "market_value": -127.0, "delta": 0.196, "gamma": 0.005, "theta": -0.001, "vega": 0.005, "unrealized_pnl": -102.0, "expiry": "2026-10-16", "strike": 5},
    {"section": "Options", "ticker": "ACHR Jun'26 23C", "underlying": "ACHR", "instrument": "call", "side": "short", "qty": -5, "avg_price": 0.277, "last": 0.00, "market_value": 0.0, "delta": 0.000, "gamma": 0.000, "theta": 0.000, "vega": 0.000, "unrealized_pnl": -104.0, "expiry": "2026-06-18", "strike": 23},
    {"section": "Options", "ticker": "NEXT Jan'25 17C", "underlying": "NEXT", "instrument": "call", "side": "short", "qty": -5, "avg_price": 0.287, "last": 0.14, "market_value": -67.0, "delta": 0.113, "gamma": 0.013, "theta": -0.002, "vega": 0.013, "unrealized_pnl": -40.0, "expiry": "2025-01-17", "strike": 17},
    {"section": "Options", "ticker": "SG Jan'27 15C", "underlying": "SG", "instrument": "call", "side": "short", "qty": -2, "avg_price": 1.451, "last": 1.05, "market_value": -146.0, "delta": 0.336, "gamma": 0.025, "theta": -0.005, "vega": 0.025, "unrealized_pnl": -72.0, "expiry": "2027-01-15", "strike": 15},
])

uploaded = st.sidebar.file_uploader("Upload portfolio CSV", type=["csv"])
df = pd.read_csv(uploaded) if uploaded is not None else sample.copy()

for col in ["market_value", "unrealized_pnl", "delta", "gamma", "theta", "vega", "qty", "last", "avg_price", "strike"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

for col in ["market_value", "unrealized_pnl", "delta", "gamma", "theta", "vega", "qty", "last", "avg_price"]:
    if col in df.columns:
        df[col] = df[col].fillna(0)

if "strike" in df.columns:
    df["strike"] = df["strike"].fillna(np.nan)

required_defaults = {
    "section": "",
    "ticker": "",
    "underlying": "",
    "instrument": "",
    "side": "",
    "expiry": "",
}
for col, default in required_defaults.items():
    if col not in df.columns:
        df[col] = default

if "theta" not in df.columns:
    df["theta"] = 0.0
if "vega" not in df.columns:
    df["vega"] = 0.0
if "gamma" not in df.columns:
    df["gamma"] = 0.0
if "delta" not in df.columns:
    df["delta"] = 0.0

st.sidebar.header("Filters")
sections = ["All"] + sorted([x for x in df["section"].dropna().unique().tolist() if str(x).strip() != ""])
selected_section = st.sidebar.selectbox("Section", sections)
if selected_section != "All":
    df = df[df["section"] == selected_section].copy()

underlyings = ["All"] + sorted([x for x in df["underlying"].dropna().unique().tolist() if str(x).strip() != ""])
selected_underlying = st.sidebar.selectbox("Underlying", underlyings)
if selected_underlying != "All":
    df = df[df["underlying"] == selected_underlying].copy()

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Positions", "Theta Risk", "History"])

with tab1:
    total_mv = float(df["market_value"].sum()) if "market_value" in df.columns else 0.0
    total_pnl = float(df["unrealized_pnl"].sum()) if "unrealized_pnl" in df.columns else 0.0
    total_theta = float(df["theta"].sum()) if "theta" in df.columns else 0.0
    total_vega = float(df["vega"].sum()) if "vega" in df.columns else 0.0
    total_delta = float(df["delta"].sum()) if "delta" in df.columns else 0.0
    total_gamma = float(df["gamma"].sum()) if "gamma" in df.columns else 0.0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Market Value", f"${total_mv:,.0f}")
    c2.metric("Unrealized P&L", f"${total_pnl:,.0f}")
    c3.metric("Theta", f"{total_theta:,.3f}")
    c4.metric("Delta", f"{total_delta:,.3f}")
    c5.metric("Gamma", f"{total_gamma:,.3f}")
    c6.metric("Vega", f"{total_vega:,.3f}")

    if "underlying" in df.columns and len(df):
        top_theta = df.groupby("underlying", as_index=False)[["theta", "vega", "delta", "gamma"]].sum().sort_values("theta", ascending=False)
        fig = px.bar(top_theta, x="underlying", y="theta", color="vega", title="Theta by Underlying")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    show_cols = [c for c in ["section", "ticker", "underlying", "instrument", "side", "qty", "avg_price", "last", "market_value", "delta", "gamma", "theta", "vega", "unrealized_pnl", "expiry", "strike"] if c in df.columns]
    st.dataframe(df[show_cols], use_container_width=True)

    if "underlying" in df.columns and "market_value" in df.columns and len(df):
        mv = df.groupby("underlying", as_index=False)["market_value"].sum().sort_values("market_value", ascending=False)
        fig = px.bar(mv, x="underlying", y="market_value", title="Market Value by Underlying")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Theta Income Analysis")

    shorts = df[df["side"] == "short"].copy() if "side" in df.columns else df.iloc[0:0].copy()
    longs = df[df["side"] == "long"].copy() if "side" in df.columns else df.iloc[0:0].copy()

    a, b = st.columns(2)
    a.metric("Short Legs", len(shorts))
    b.metric("Long Legs", len(longs))

    if len(df):
        risk = df.copy()
        risk["theta_abs"] = risk["theta"].abs()
        risk["theta_per_vega"] = np.where(risk["vega"].abs() > 0, risk["theta"] / risk["vega"].abs(), np.nan)
        risk["theta_per_gamma"] = np.where(risk["gamma"].abs() > 0, risk["theta"] / risk["gamma"].abs(), np.nan)
        risk_cols = [c for c in ["underlying", "ticker", "side", "theta", "delta", "gamma", "vega", "theta_per_vega", "theta_per_gamma", "unrealized_pnl"] if c in risk.columns]
        st.dataframe(risk[risk_cols], use_container_width=True)

    if "underlying" in df.columns and len(df):
        theta_by_u = df.groupby("underlying", as_index=False)[["theta", "vega", "gamma", "delta"]].sum().sort_values("theta", ascending=False)
        fig = px.bar(theta_by_u, x="underlying", y="theta", color="vega", title="Theta vs Vega by Underlying")
        st.plotly_chart(fig, use_container_width=True)

        if "instrument" in df.columns:
            heat = df.pivot_table(index="underlying", columns="instrument", values="theta", aggfunc="sum", fill_value=0)
            if heat.shape[0] > 0 and heat.shape[1] > 0:
                fig2 = go.Figure(data=go.Heatmap(z=heat.values, x=heat.columns.tolist(), y=heat.index.tolist(), colorscale="RdYlGn"))
                fig2.update_layout(title="Theta Heatmap by Underlying and Instrument")
                st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.subheader("Snapshot History")
    hist_file = DATA_DIR / "snapshots.csv"

    snapshot = df.copy()
    snapshot["timestamp"] = datetime.now().isoformat(timespec="seconds")

    if st.button("Save Snapshot"):
        if hist_file.exists():
            old = pd.read_csv(hist_file)
            out = pd.concat([old, snapshot], ignore_index=True)
        else:
            out = snapshot
        out.to_csv(hist_file, index=False)
        st.success("Snapshot saved.")

    if hist_file.exists():
        hist = pd.read_csv(hist_file)
        st.dataframe(hist, use_container_width=True)

        if {"timestamp", "theta"}.issubset(hist.columns):
            grp = hist.groupby("timestamp", as_index=False)["theta"].sum()
            fig = px.line(grp, x="timestamp", y="theta", title="Theta Over Time")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No snapshots saved yet.")
