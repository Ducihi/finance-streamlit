from __future__ import annotations

from datetime import date, timedelta
from typing import BinaryIO

import pandas as pd
import yfinance as yf


STANDARD_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]


class DataError(Exception):
    """Raised when a data source cannot produce a usable price table."""


def normalize_columns(data: pd.DataFrame) -> pd.DataFrame:
    normalized = data.copy()

    if isinstance(normalized.columns, pd.MultiIndex):
        normalized.columns = [column[0] for column in normalized.columns]

    normalized = normalized.reset_index() if "Date" not in normalized.columns else normalized
    normalized = normalized.rename(columns={column: str(column).strip() for column in normalized.columns})

    if "Datetime" in normalized.columns and "Date" not in normalized.columns:
        normalized = normalized.rename(columns={"Datetime": "Date"})

    missing_required = {"Date", "Close"} - set(normalized.columns)
    if missing_required:
        missing = ", ".join(sorted(missing_required))
        raise DataError(
            "\u8cc7\u6599\u7f3a\u5c11\u5fc5\u8981\u6b04\u4f4d\uff1a"
            f"{missing}\u3002\u8acb\u78ba\u8a8d CSV \u81f3\u5c11\u5305\u542b Date \u8207 Close\u3002"
        )

    normalized["Date"] = pd.to_datetime(normalized["Date"], errors="coerce").dt.tz_localize(None)
    normalized = normalized.dropna(subset=["Date", "Close"]).sort_values("Date")

    for column in ["Open", "High", "Low", "Adj Close"]:
        if column not in normalized.columns:
            normalized[column] = normalized["Close"]

    if "Volume" not in normalized.columns:
        normalized["Volume"] = pd.NA

    for column in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    normalized = normalized[STANDARD_COLUMNS]
    if normalized.empty:
        raise DataError("\u8cc7\u6599\u70ba\u7a7a\u6216\u7121\u6cd5\u89e3\u6790\uff0c\u8acb\u78ba\u8a8d\u65e5\u671f\u8207\u50f9\u683c\u6b04\u4f4d\u5167\u5bb9\u3002")

    return normalized


def load_yahoo_data(symbol: str, start_date: date, end_date: date) -> pd.DataFrame:
    if not symbol.strip():
        raise DataError("\u8acb\u8f38\u5165\u5546\u54c1\u4ee3\u865f\u3002")

    try:
        raw_data = yf.download(
            symbol,
            start=start_date,
            end=end_date + timedelta(days=1),
            progress=False,
            auto_adjust=False,
        )
    except Exception as error:  # pragma: no cover - yfinance raises several transport-level types.
        raise DataError(f"Yahoo Finance \u67e5\u8a62\u5931\u6557\uff1a{error}") from error

    if raw_data.empty:
        raise DataError("Yahoo Finance \u67e5\u7121\u8cc7\u6599\uff0c\u8acb\u78ba\u8a8d\u5546\u54c1\u4ee3\u865f\u8207\u65e5\u671f\u5340\u9593\u3002")

    return normalize_columns(raw_data)


def load_csv_data(file: BinaryIO) -> pd.DataFrame:
    try:
        raw_data = pd.read_csv(file)
    except Exception as error:
        raise DataError(f"CSV \u8b80\u53d6\u5931\u6557\uff1a{error}") from error

    return normalize_columns(raw_data)


def filter_date_range(data: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    filtered = data[(data["Date"] >= start) & (data["Date"] <= end)].copy()
    if filtered.empty:
        raise DataError("CSV \u5728\u6307\u5b9a\u65e5\u671f\u5340\u9593\u5167\u6c92\u6709\u8cc7\u6599\u3002")
    return filtered
