# Theta Income Portfolio

A Streamlit dashboard for monitoring an income-focused options portfolio.

## What it shows

- Overview metrics
- Positions table
- Theta, delta, gamma, and vega by underlying
- Heatmap of theta by instrument
- Snapshot history saved locally

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to GitHub + Streamlit Community Cloud

1. Create a GitHub repo.
2. Add `app.py`, `requirements.txt`, and `README.md`.
3. Push the repo.
4. Open Streamlit Community Cloud.
5. Select your repo and `app.py`.
6. Deploy.

## CSV columns

Recommended columns:

- `section`
- `ticker`
- `underlying`
- `instrument`
- `side`
- `qty`
- `avg_price`
- `last`
- `market_value`
- `delta`
- `gamma`
- `theta`
- `vega`
- `unrealized_pnl`
- `expiry`
- `strike`

## Next upgrades

- Pull live options chains with yfinance.
- Add strike-by-expiry heatmaps.
- Add per-ticker stress tests.
- Add alerts for large short gamma or vega exposure.
