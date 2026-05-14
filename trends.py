from __future__ import annotations

from datetime import date
from time import sleep

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
    trends = pd.DataFrame()
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            sleep(2)
            client = TrendReq(
                hl="zh-TW",
                tz=480,
                timeout=(10, 25),
                requests_args={
                    "headers": {
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/124.0 Safari/537.36"
                        )
                    }
                },
            )
            client.build_payload([keyword], timeframe=timeframe, geo=geo)
            trends = client.interest_over_time()
            break
        except Exception as error:  # pragma: no cover - pytrends surfaces network/API errors.
            last_error = error
            sleep(1.5 * (attempt + 1))

    if trends.empty and last_error is not None:
        raise DataError(
            "Google Trends \u67e5\u8a62\u5931\u6557\uff1a"
            f"{last_error}. \u8acb\u7a0d\u5f8c\u91cd\u8a66\uff0c\u6216\u78ba\u8a8d\u95dc\u9375\u5b57\u8207\u5340\u57df\u8a2d\u5b9a\u3002"
        ) from last_error

    if trends.empty or keyword not in trends.columns:
        raise DataError("Google Trends \u67e5\u7121\u8cc7\u6599\uff0c\u8acb\u8abf\u6574\u95dc\u9375\u5b57\u6216\u65e5\u671f\u5340\u9593\u3002")

    trends = trends.drop(columns=["isPartial"], errors="ignore")
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
