from __future__ import annotations

from datetime import date, timedelta
from html import escape
from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from data import DataError, filter_date_range, load_csv_data, load_yahoo_data
from indicators import add_ema, add_macd, add_rsi, add_sma
from trends import GEO_OPTIONS, load_google_trends, merge_google_trends


TEXT = {
    "app_title": "\u91d1\u878d\u6578\u64da\u67e5\u8a62\u5e73\u53f0",
    "disclaimer": "\u672c\u5de5\u5177\u7528\u65bc\u7814\u7a76\u8207\u6559\u80b2\u7528\u9014\uff0c\u8cc7\u6599\u8207\u5716\u8868\u4e0d\u69cb\u6210\u6295\u8cc7\u5efa\u8b70\u3002",
    "research_only": "\u7814\u7a76\u7528\u9014",
    "query_settings": "\u67e5\u8a62\u8a2d\u5b9a",
    "data_source": "\u8cc7\u6599\u4f86\u6e90",
    "csv_upload": "CSV \u4e0a\u50b3",
    "allow_weekends": "\u5141\u8a31\u9031\u672b\u8cc7\u6599",
    "analysis_dates": "\u5206\u6790\u65e5\u671f",
    "symbol": "\u5546\u54c1\u4ee3\u865f",
    "symbol_placeholder": "\u4f8b\u5982 SPY\u3001AAPL\u30012330.TW",
    "data_name": "\u8cc7\u6599\u540d\u7a31",
    "indicator_settings": "\u6280\u8853\u6307\u6a19",
    "trend_settings": "Google Trends",
    "enable_google_trends": "\u6293\u53d6 Google Trends",
    "trend_keyword": "Google Trends \u95dc\u9375\u5b57",
    "trend_geo": "\u641c\u5c0b\u5340\u57df",
    "global": "\u5168\u7403",
    "taiwan": "\u53f0\u7063",
    "us": "\u7f8e\u570b",
    "sma": "SMA \u5747\u7dda",
    "short_sma": "\u77ed\u671f SMA",
    "long_sma": "\u9577\u671f SMA",
    "ema": "EMA \u6307\u6578\u5747\u7dda",
    "ema_window": "EMA \u9031\u671f",
    "rsi_window": "RSI \u9031\u671f",
    "macd": "MACD",
    "macd_fast": "MACD \u5feb\u7dda EMA",
    "macd_slow": "MACD \u6162\u7dda EMA",
    "macd_signal": "MACD \u8a0a\u865f\u7dda",
    "volume": "\u6210\u4ea4\u91cf",
    "complete_dates": "\u8acb\u9078\u64c7\u5b8c\u6574\u7684\u958b\u59cb\u8207\u7d50\u675f\u65e5\u671f\u3002",
    "date_error": "\u7d50\u675f\u65e5\u671f\u4e0d\u53ef\u65e9\u65bc\u958b\u59cb\u65e5\u671f\u3002",
    "macd_error": "MACD \u5feb\u7dda EMA \u5fc5\u9808\u5c0f\u65bc\u6162\u7dda EMA\u3002",
    "symbol_error": "\u8acb\u8f38\u5165\u5546\u54c1\u4ee3\u865f\u6216\u8cc7\u6599\u540d\u7a31\u3002",
    "upload_hint": "\u8acb\u4e0a\u50b3 CSV \u6a94\u6848\uff0c\u81f3\u5c11\u5305\u542b Date \u8207 Close \u6b04\u4f4d\u3002",
    "empty_data": "\u67e5\u7121\u7b26\u5408\u689d\u4ef6\u7684\u8cc7\u6599\uff0c\u8acb\u8abf\u6574\u4ee3\u865f\u3001\u65e5\u671f\u6216\u4e0a\u50b3\u5167\u5bb9\u3002",
    "rows": "\u8cc7\u6599\u7b46\u6578",
    "date_span": "\u8d77\u8a16\u65e5\u671f",
    "last_close": "\u6700\u65b0\u6536\u76e4\u50f9",
    "period_return": "\u671f\u9593\u5831\u916c",
    "highest": "\u6700\u9ad8\u50f9",
    "lowest": "\u6700\u4f4e\u50f9",
    "avg_volume": "\u5e73\u5747\u6210\u4ea4\u91cf",
    "close": "\u6536\u76e4\u50f9",
    "price": "\u50f9\u683c",
    "date": "\u65e5\u671f",
    "price_trend": "\u50f9\u683c\u8d70\u52e2",
    "price_chart": "\u50f9\u683c\u5716\u8868",
    "indicator_tab": "\u6280\u8853\u6307\u6a19",
    "trend_tab": "Google Trends",
    "data_preview": "\u8cc7\u6599\u9810\u89bd",
    "enable_indicator": "\u8acb\u5728\u5074\u908a\u6b04\u555f\u7528 RSI\u3001MACD \u6216\u6210\u4ea4\u91cf\u6307\u6a19\u3002",
    "trend_unavailable": "Google Trends \u5c1a\u672a\u8f09\u5165\uff0c\u8acb\u555f\u7528\u6293\u53d6\u4e26\u78ba\u8a8d\u95dc\u9375\u5b57\u3002",
    "trend_rate_limit_help": "Google Trends \u5728\u96f2\u7aef\u53ef\u80fd\u56e0 IP \u9650\u6d41\u800c\u56de\u50b3 429\u3002\u50f9\u683c\u8207\u6280\u8853\u6307\u6a19\u4ecd\u53ef\u6b63\u5e38\u4f7f\u7528\uff0c\u8acb\u7a0d\u5f8c\u518d\u91cd\u8a66\u6216\u95dc\u9589 Google Trends \u6293\u53d6\u3002",
    "trend_value": "\u641c\u5c0b\u71b1\u5ea6",
    "trend_rows": "Google Trends \u8cc7\u6599\u7b46\u6578",
    "download_csv": "\u4e0b\u8f09 CSV",
    "to": "\u81f3",
}


st.set_page_config(
    page_title=TEXT["app_title"],
    page_icon="\U0001f4c8",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_google_trends(keyword: str, start_date: date, end_date: date, geo: str) -> pd.DataFrame:
    return load_google_trends(keyword, start_date, end_date, geo)


def apply_layout_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --panel-bg: #ffffff;
            --muted-bg: #f7f9fc;
            --border: #e5e7eb;
            --text: #202638;
            --muted: #687386;
            --accent: #ef4444;
            --accent-soft: #fff1f2;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f6f8fb 0%, #eef2f7 100%);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem 1.1rem;
        }

        div[data-testid="stMetric"] label {
            color: var(--muted);
        }

        .dashboard-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 1.25rem;
            margin: 0 0 1rem;
            padding: 1.1rem 1.25rem;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .dashboard-title {
            margin: 0;
            color: var(--text);
            font-size: clamp(1.6rem, 2.2vw, 2.2rem);
            font-weight: 750;
            line-height: 1.15;
        }

        .dashboard-subtitle {
            margin-top: 0.45rem;
            color: var(--muted);
            font-size: 0.98rem;
        }

        .dashboard-badge {
            flex: 0 0 auto;
            color: #991b1b;
            background: var(--accent-soft);
            border: 1px solid #fecdd3;
            border-radius: 999px;
            padding: 0.45rem 0.8rem;
            font-size: 0.9rem;
            font-weight: 650;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 0.85rem 0 1.35rem;
        }

        .metric-card {
            min-height: 104px;
            padding: 1rem;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.88rem;
            font-weight: 650;
            margin-bottom: 0.45rem;
        }

        .metric-value {
            color: var(--text);
            font-size: clamp(1.35rem, 2.1vw, 2.2rem);
            font-weight: 720;
            line-height: 1.15;
            overflow-wrap: anywhere;
        }

        .metric-value.is-long {
            font-size: clamp(1.05rem, 1.35vw, 1.35rem);
            line-height: 1.3;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--border);
        }

        .stTabs [data-baseweb="tab"] {
            height: 2.8rem;
            padding: 0 0.9rem;
            border-radius: 8px 8px 0 0;
        }

        .stAlert {
            border-radius: 8px;
        }

        @media (max-width: 1100px) {
            .metric-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .dashboard-header {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        @media (max-width: 640px) {
            .block-container {
                padding-top: 1rem;
            }
            .metric-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_header(symbol: str, source: object, data: pd.DataFrame) -> None:
    date_range = f"{data['Date'].min():%Y-%m-%d} {TEXT['to']} {data['Date'].max():%Y-%m-%d}"
    st.markdown(
        f"""
        <section class="dashboard-header">
            <div>
                <h1 class="dashboard-title">{escape(symbol)} - {escape(str(source))}</h1>
                <div class="dashboard-subtitle">{escape(date_range)} | {len(data):,} {escape(TEXT["rows"])}</div>
            </div>
            <div class="dashboard-badge">{escape(TEXT["research_only"])}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(summary: dict[str, str]) -> None:
    cards = []
    for label, value in summary.items():
        value_class = "metric-value is-long" if label == TEXT["date_span"] else "metric-value"
        cards.append(
            f"""
            <div class="metric-card">
                <div class="metric-label">{escape(label)}</div>
                <div class="{value_class}">{escape(value)}</div>
            </div>
            """
        )
    st.markdown(f'<section class="metric-grid">{"".join(cards)}</section>', unsafe_allow_html=True)


def format_number(value: float | int | None, decimals: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.{decimals}f}"


def format_percent(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value * 100:,.2f}%"


def resample_calendar_days(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return data

    daily_index = pd.date_range(data["Date"].min(), data["Date"].max(), freq="D")
    resampled = data.set_index("Date").reindex(daily_index)
    resampled.index.name = "Date"

    price_columns = ["Open", "High", "Low", "Close", "Adj Close"]
    available_price_columns = [column for column in price_columns if column in resampled.columns]
    resampled[available_price_columns] = resampled[available_price_columns].ffill()

    if "Volume" in resampled.columns:
        resampled["Volume"] = resampled["Volume"].fillna(0)

    return resampled.reset_index()


def calculate_summary(data: pd.DataFrame) -> dict[str, str]:
    close_values = data["Close"].dropna()
    first_close = close_values.iloc[0] if not close_values.empty else None
    last_close = close_values.iloc[-1] if not close_values.empty else None
    period_return = None
    if first_close and last_close:
        period_return = (last_close / first_close) - 1

    volume = data["Volume"] if "Volume" in data.columns else pd.Series(dtype="float64")

    return {
        TEXT["rows"]: f"{len(data):,}",
        TEXT["date_span"]: f"{data['Date'].min():%Y-%m-%d} {TEXT['to']} {data['Date'].max():%Y-%m-%d}",
        TEXT["last_close"]: format_number(last_close),
        TEXT["period_return"]: format_percent(period_return),
        TEXT["highest"]: format_number(data["High"].max() if "High" in data.columns else data["Close"].max()),
        TEXT["lowest"]: format_number(data["Low"].min() if "Low" in data.columns else data["Close"].min()),
        TEXT["avg_volume"]: format_number(volume.mean(), 0) if not volume.dropna().empty else "-",
    }


def build_price_chart(data: pd.DataFrame, symbol: str, show_sma: bool, show_ema: bool) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            name=TEXT["close"],
            line={"color": "#2563eb", "width": 2},
        )
    )

    if show_sma:
        for column, color in [("SMA Short", "#16a34a"), ("SMA Long", "#dc2626")]:
            if column in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data["Date"],
                        y=data[column],
                        mode="lines",
                        name=column,
                        line={"color": color, "width": 1.5},
                    )
                )

    if show_ema and "EMA" in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["EMA"],
                mode="lines",
                name="EMA",
                line={"color": "#9333ea", "width": 1.5},
            )
        )

    fig.update_layout(
        title=f"{symbol} {TEXT['price_trend']}",
        height=520,
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        xaxis_title=TEXT["date"],
        yaxis_title=TEXT["price"],
    )
    return fig


def build_indicator_chart(data: pd.DataFrame, show_rsi: bool, show_macd: bool, show_volume: bool) -> go.Figure:
    enabled_sections = ["price"]
    if show_rsi and "RSI" in data.columns:
        enabled_sections.append("rsi")
    if show_macd and "MACD" in data.columns:
        enabled_sections.append("macd")
    if show_volume and "Volume" in data.columns:
        enabled_sections.append("volume")

    row_count = len(enabled_sections)
    row_heights = [0.42] + [0.58 / (row_count - 1)] * (row_count - 1) if row_count > 1 else [1.0]
    fig = make_subplots(
        rows=row_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=row_heights,
    )
    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            name=TEXT["close"],
            line={"color": "#2563eb", "width": 2},
        ),
        row=1,
        col=1,
    )

    row_index = 2
    if "rsi" in enabled_sections:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["RSI"],
                mode="lines",
                name="RSI",
                line={"color": "#f97316", "width": 1.6},
            ),
            row=row_index,
            col=1,
        )
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=row_index, col=1)
        row_index += 1

    if "macd" in enabled_sections:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["MACD"],
                mode="lines",
                name="MACD",
                line={"color": "#7c3aed", "width": 1.6},
            ),
            row=row_index,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["MACD Signal"],
                mode="lines",
                name="Signal",
                line={"color": "#ea580c", "width": 1.4},
            ),
            row=row_index,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=data["Date"],
                y=data["MACD Histogram"],
                name="Histogram",
                marker_color="#94a3b8",
                opacity=0.65,
            ),
            row=row_index,
            col=1,
        )
        fig.update_yaxes(title_text="MACD", row=row_index, col=1)
        row_index += 1

    if "volume" in enabled_sections:
        fig.add_trace(
            go.Bar(
                x=data["Date"],
                y=data["Volume"],
                name=TEXT["volume"],
                marker_color="#64748b",
                opacity=0.55,
            ),
            row=row_index,
            col=1,
        )
        fig.update_yaxes(title_text=TEXT["volume"], row=row_index, col=1)

    fig.update_yaxes(title_text=TEXT["price"], row=1, col=1)
    fig.update_xaxes(title_text=TEXT["date"], row=row_count, col=1)
    fig.update_layout(
        title=TEXT["indicator_tab"],
        height=680 if row_count >= 3 else 560,
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    return fig


def build_trend_chart(data: pd.DataFrame, symbol: str, keyword: str) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            name=TEXT["close"],
            line={"color": "#2563eb", "width": 2},
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Google Trend"],
            mode="lines",
            name=f"{keyword} Google Trend",
            line={"color": "#dc2626", "width": 1.8},
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title=f"{symbol} - Google Trends",
        height=520,
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_yaxes(title_text=TEXT["price"], secondary_y=False)
    fig.update_yaxes(title_text=TEXT["trend_value"], secondary_y=True, range=[0, 100])
    fig.update_xaxes(title_text=TEXT["date"])
    return fig


def available_indicator_columns(data: pd.DataFrame) -> list[str]:
    columns = ["Date"]
    for column in ["RSI", "MACD", "MACD Signal", "MACD Histogram"]:
        if column in data.columns:
            columns.append(column)
    return columns


def sidebar_settings() -> dict[str, object]:
    st.sidebar.header(TEXT["query_settings"])

    source = st.sidebar.radio(TEXT["data_source"], ["Yahoo Finance", TEXT["csv_upload"]], horizontal=True)
    allow_weekends = st.sidebar.checkbox(TEXT["allow_weekends"], value=False)

    default_end = date.today()
    default_start = default_end - timedelta(days=365 * 3)
    date_range = st.sidebar.date_input(TEXT["analysis_dates"], (default_start, default_end))

    symbol = "CSV"
    uploaded_file = None
    if source == "Yahoo Finance":
        symbol = st.sidebar.text_input(TEXT["symbol"], value="SPY", placeholder=TEXT["symbol_placeholder"])
    else:
        uploaded_file = st.sidebar.file_uploader(TEXT["csv_upload"], type=["csv"])
        symbol = st.sidebar.text_input(TEXT["data_name"], value="CSV Data")

    st.sidebar.divider()
    st.sidebar.header(TEXT["indicator_settings"])

    show_sma = st.sidebar.checkbox(TEXT["sma"], value=True)
    sma_short = st.sidebar.number_input(TEXT["short_sma"], min_value=2, max_value=250, value=20, step=1)
    sma_long = st.sidebar.number_input(TEXT["long_sma"], min_value=2, max_value=400, value=60, step=1)

    show_ema = st.sidebar.checkbox(TEXT["ema"], value=False)
    ema_window = st.sidebar.number_input(TEXT["ema_window"], min_value=2, max_value=250, value=20, step=1)

    show_rsi = st.sidebar.checkbox("RSI", value=True)
    rsi_window = st.sidebar.number_input(TEXT["rsi_window"], min_value=2, max_value=100, value=14, step=1)

    show_macd = st.sidebar.checkbox(TEXT["macd"], value=True)
    macd_fast = st.sidebar.number_input(TEXT["macd_fast"], min_value=2, max_value=100, value=12, step=1)
    macd_slow = st.sidebar.number_input(TEXT["macd_slow"], min_value=3, max_value=200, value=26, step=1)
    macd_signal = st.sidebar.number_input(TEXT["macd_signal"], min_value=2, max_value=100, value=9, step=1)

    show_volume = st.sidebar.checkbox(TEXT["volume"], value=True)

    st.sidebar.divider()
    st.sidebar.header(TEXT["trend_settings"])
    enable_google_trends = st.sidebar.checkbox(TEXT["enable_google_trends"], value=True)
    trend_keyword = st.sidebar.text_input(TEXT["trend_keyword"], value=symbol)
    geo_labels = {
        TEXT["global"]: GEO_OPTIONS["Global"],
        TEXT["taiwan"]: GEO_OPTIONS["Taiwan"],
        TEXT["us"]: GEO_OPTIONS["United States"],
    }
    selected_geo_label = st.sidebar.selectbox(TEXT["trend_geo"], list(geo_labels.keys()))

    return {
        "source": source,
        "allow_weekends": allow_weekends,
        "date_range": date_range,
        "symbol": symbol.strip(),
        "uploaded_file": uploaded_file,
        "show_sma": show_sma,
        "sma_short": int(sma_short),
        "sma_long": int(sma_long),
        "show_ema": show_ema,
        "ema_window": int(ema_window),
        "show_rsi": show_rsi,
        "rsi_window": int(rsi_window),
        "show_macd": show_macd,
        "macd_fast": int(macd_fast),
        "macd_slow": int(macd_slow),
        "macd_signal": int(macd_signal),
        "show_volume": show_volume,
        "enable_google_trends": enable_google_trends,
        "trend_keyword": trend_keyword.strip(),
        "trend_geo": geo_labels[selected_geo_label],
    }


def main() -> None:
    apply_layout_styles()
    settings = sidebar_settings()

    date_range = settings["date_range"]
    if not isinstance(date_range, tuple) or len(date_range) != 2:
        st.info(TEXT["complete_dates"])
        return

    start_date, end_date = date_range
    if start_date > end_date:
        st.error(TEXT["date_error"])
        return

    if settings["show_macd"] and int(settings["macd_fast"]) >= int(settings["macd_slow"]):
        st.error(TEXT["macd_error"])
        return

    symbol = str(settings["symbol"]).upper()
    if not symbol:
        st.error(TEXT["symbol_error"])
        return

    try:
        if settings["source"] == "Yahoo Finance":
            data = load_yahoo_data(symbol, start_date, end_date)
        else:
            if settings["uploaded_file"] is None:
                st.info(TEXT["upload_hint"])
                return
            data = load_csv_data(settings["uploaded_file"])
            data = filter_date_range(data, start_date, end_date)
    except DataError as error:
        st.error(str(error))
        return

    if data.empty:
        st.warning(TEXT["empty_data"])
        return

    if settings["allow_weekends"]:
        data = resample_calendar_days(data)

    if settings["show_sma"]:
        data = add_sma(data, int(settings["sma_short"]), "SMA Short")
        data = add_sma(data, int(settings["sma_long"]), "SMA Long")
    if settings["show_ema"]:
        data = add_ema(data, int(settings["ema_window"]), "EMA")
    if settings["show_rsi"]:
        data = add_rsi(data, int(settings["rsi_window"]), "RSI")
    if settings["show_macd"]:
        data = add_macd(
            data,
            int(settings["macd_fast"]),
            int(settings["macd_slow"]),
            int(settings["macd_signal"]),
        )

    trend_error = None
    trends_data = pd.DataFrame()
    if settings["enable_google_trends"]:
        try:
            trends_data = cached_google_trends(
                str(settings["trend_keyword"]),
                start_date,
                end_date,
                str(settings["trend_geo"]),
            )
            data = merge_google_trends(data, trends_data)
        except DataError as error:
            trend_error = str(error)

    render_dashboard_header(symbol, settings["source"], data)
    summary = calculate_summary(data)
    render_metric_cards(summary)

    price_tab, indicator_tab, trend_tab, data_tab = st.tabs(
        [TEXT["price_chart"], TEXT["indicator_tab"], TEXT["trend_tab"], TEXT["data_preview"]]
    )

    with price_tab:
        st.plotly_chart(
            build_price_chart(
                data,
                symbol,
                bool(settings["show_sma"]),
                bool(settings["show_ema"]),
            ),
            use_container_width=True,
        )

    with indicator_tab:
        if not settings["show_rsi"] and not settings["show_macd"] and not settings["show_volume"]:
            st.info(TEXT["enable_indicator"])
        else:
            st.plotly_chart(
                build_indicator_chart(
                    data,
                    bool(settings["show_rsi"]),
                    bool(settings["show_macd"]),
                    bool(settings["show_volume"]),
                ),
                use_container_width=True,
            )
            indicator_columns = available_indicator_columns(data)
            if len(indicator_columns) > 1:
                st.dataframe(
                    data[indicator_columns].dropna(subset=indicator_columns[1:], how="all"),
                    use_container_width=True,
                    hide_index=True,
                )

    with trend_tab:
        if trend_error:
            st.warning(trend_error)
            st.info(TEXT["trend_rate_limit_help"])
        elif "Google Trend" not in data.columns or data["Google Trend"].dropna().empty:
            st.info(TEXT["trend_unavailable"])
        else:
            st.metric(TEXT["trend_rows"], f"{len(trends_data):,}")
            st.plotly_chart(
                build_trend_chart(data, symbol, str(settings["trend_keyword"])),
                use_container_width=True,
            )
            st.dataframe(
                trends_data.rename(columns={"Date": "Trend Date"}),
                use_container_width=True,
                hide_index=True,
            )

    with data_tab:
        st.dataframe(data, use_container_width=True, hide_index=True)
        csv = data.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            TEXT["download_csv"],
            data=csv,
            file_name=f"{symbol.lower()}_financial_data.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
