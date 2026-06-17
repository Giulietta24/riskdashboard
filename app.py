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

sample = pd.DataF
