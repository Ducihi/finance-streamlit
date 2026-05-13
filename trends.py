from __future__ import annotations

from datetime import date

import pandas as pd
from pytrends.request import TrendReq

from data import DataError


GEO_OPTIONS = {
    "Global": "",
    "Taiwan": "TW",
    "United States": "US",
}


def load_google_trends(keyword: str, start_date: date, end_date: date, geo: str) -> pd.DataFrame:
    if not keyword.strip():
        raise DataError("\u8acb\u8f38\u5165 Google Trends \u95dc\u9375\u5b57\u3002")

    timeframe = f"{start_date:%Y-%m-%d} {end_date:%Y-%m-%d}"
    try:
        client = TrendReq(hl="zh-TW", tz=480)
        client.build_payload([keyword], timeframe=timeframe, geo=geo)
        trends = client.interest_over_time()
    except Exception as error:  # pragma: no cover - pytrends surfaces network/API errors.
        raise DataError(f"Google Trends \u67e5\u8a62\u5931\u6557\uff1a{error}") from error

    if trends.empty or keyword not in trends.columns:
        raise DataError("Google Trends \u67e5\u7121\u8cc7\u6599\uff0c\u8acb\u8abf\u6574\u95dc\u9375\u5b57\u6216\u65e5\u671f\u5340\u9593\u3002")

    output = trends.reset_index().rename(columns={"date": "Date", keyword: "Google Trend"})
    output["Date"] = pd.to_datetime(output["Date"]).dt.tz_localize(None)
    output["Google Trend"] = pd.to_numeric(output["Google Trend"], errors="coerce")
    return output[["Date", "Google Trend"]].dropna(subset=["Date"])


def merge_google_trends(price_data: pd.DataFrame, trends_data: pd.DataFrame) -> pd.DataFrame:
    if price_data.empty or trends_data.empty:
        return price_data

    prices = price_data.sort_values("Date").copy()
    trends = trends_data.sort_values("Date").copy()
    return pd.merge_asof(prices, trends, on="Date", direction="backward")
