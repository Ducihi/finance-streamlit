# Financial Data Query Platform

Streamlit app for querying financial price data, technical indicators, and Google Trends interest.

## Install

```powershell
pip install -r requirements.txt
```

## Run

```powershell
streamlit run finance.py
```

The legacy command `streamlit run app.py` still works through a compatibility wrapper.

## Public Website

To keep the site available for other people at any time, deploy it to Streamlit Community Cloud with `finance.py` as the entrypoint file. See `DEPLOY.md`.

## Features

- Yahoo Finance daily OHLCV data
- CSV upload
- SMA, EMA, RSI, and MACD calculations
- Google Trends keyword interest
- Downloadable CSV with price data, indicators, and trend data

## CSV Format

Required columns:

- `Date`
- `Close`

Optional columns:

- `Open`
- `High`
- `Low`
- `Adj Close`
- `Volume`

If optional price columns are missing, the app fills them from `Close`. If `Volume` is missing, it remains empty.
