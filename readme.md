# Portfolio Risk Dashboard

A simple Streamlit starter for reviewing portfolio holdings and adding risk analytics.

## Features

- Upload a CSV of holdings.
- View market value by ticker.
- See simple exposure breakdowns.
- Extend it with options Greeks, stress tests, and history tracking.

## CSV format

Your uploaded file should include at least:

- `ticker`
- `qty`
- `last`

Optional fields:

- `type`
- `avg_price`
- `market_value`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to GitHub + Streamlit Cloud

1. Create a GitHub repo.
2. Add `app.py`, `requirements.txt`, and `README.md`.
3. Push the repo to GitHub.
4. Connect the repo in Streamlit Community Cloud.
5. Set `app.py` as the main file.

## Next upgrades

- Add options-chain ingestion with `yfinance`.
- Add Greeks and theta/vega summaries.
- Add a strike-by-expiration heatmap.
- Save daily snapshots to a `data/` folder.
- Add alerting for concentration and margin risk.
