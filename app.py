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
st.caption("Upload a portfolio CSV or adapt the sample layout for your broker export.")

uploaded = st.sidebar.file_uploader("Upload portfolio CSV", type=["csv"])

sample = pd.DataFrame([
    {"ticker": "SOFI", "type": "stock", "qty": 600, "avg_price": 28.31, "last": 18.47, "market_value": 11082.0},
    {"ticker": "GRAB", "type": "stock", "qty": 600, "avg_price": 5.60, "last": 3.46, "market_value": 2076.0},
    {"ticker": "SBET", "type": "stock", "qty": 500, "avg_price": 19.86, "last": 5.63, "market_value": 2815.0},
])

df = pd.read_csv(uploaded) if uploaded is not None else sample.copy()

st.subheader("Holdings")
st.dataframe(df, use_container_width=True)

required = {"qty", "last"}
if required.issubset(df.columns):
    if "market_value" not in df.columns:
        df["market_value"] = df["qty"] * df["last"]

    total_mv = float(df["market_value"].sum()) if len(df) else 0.0
    top_weight = (df["market_value"].max() / total_mv * 100) if total_mv else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Positions", len(df))
    c2.metric("Total Market Value", f"${total_mv:,.0f}")
    c3.metric("Top Weight", f"{top_weight:.1f}%")

    fig = px.bar(
        df,
        x="ticker",
        y="market_value",
        color="type" if "type" in df.columns else None,
        title="Market Value by Ticker",
    )
    st.plotly_chart(fig, use_container_width=True)

    if "type" in df.columns:
        pie = px.pie(df, names="type", values="market_value", title="Exposure by Type")
        st.plotly_chart(pie, use_container_width=True)

st.subheader("Risk Notes")
st.markdown(
    """
- Add options Greeks columns for delta, theta, and vega.
- Add a daily snapshot writer for history.
- Add stress-test scenarios for +/-5% and +/-10% moves.
- Add a ticker concentration table.
- Add short-option exposure tracking if you include options rows.
"""
)

with st.expander("Sample CSV format"):
    st.code(
        "ticker,type,qty,avg_price,last,market_value\n"
        "SOFI,stock,600,28.31,18.47,11082\n"
        "GRAB,stock,600,5.60,3.46,2076\n"
        "SBET,stock,500,19.86,5.63,2815",
        language="csv",
    )
