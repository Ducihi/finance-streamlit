from __future__ import annotations

import pandas as pd


def add_sma(data: pd.DataFrame, window: int, column_name: str) -> pd.DataFrame:
    output = data.copy()
    output[column_name] = output["Close"].rolling(window=window, min_periods=window).mean()
    return output


def add_ema(data: pd.DataFrame, window: int, column_name: str) -> pd.DataFrame:
    output = data.copy()
    output[column_name] = output["Close"].ewm(span=window, adjust=False, min_periods=window).mean()
    return output


def add_rsi(data: pd.DataFrame, window: int, column_name: str) -> pd.DataFrame:
    output = data.copy()
    delta = output["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    average_gain = gain.rolling(window=window, min_periods=window).mean()
    average_loss = loss.rolling(window=window, min_periods=window).mean()
    relative_strength = average_gain / average_loss.mask(average_loss == 0)

    output[column_name] = 100 - (100 / (1 + relative_strength))
    output.loc[average_loss == 0, column_name] = 100
    return output


def add_macd(
    data: pd.DataFrame,
    fast_window: int,
    slow_window: int,
    signal_window: int,
) -> pd.DataFrame:
    output = data.copy()
    fast_ema = output["Close"].ewm(span=fast_window, adjust=False, min_periods=fast_window).mean()
    slow_ema = output["Close"].ewm(span=slow_window, adjust=False, min_periods=slow_window).mean()

    output["MACD"] = fast_ema - slow_ema
    output["MACD Signal"] = output["MACD"].ewm(
        span=signal_window,
        adjust=False,
        min_periods=signal_window,
    ).mean()
    output["MACD Histogram"] = output["MACD"] - output["MACD Signal"]
    return output
