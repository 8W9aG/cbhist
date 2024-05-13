"""A function for fetching candles directly from coinbase."""

# pylint: disable=line-too-long
import datetime

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

MAX_CANDLES = (
    300  # This is the maximum candles the coinbase API allows at any given time.
)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=20))
def fetch_candles(product_id: str, granularity: int, start: int) -> pd.DataFrame:
    """Fetch OHLC candles for a particular time chunk."""
    end = start + granularity * MAX_CANDLES
    response = requests.get(
        f"https://api.exchange.coinbase.com/products/{product_id}/candles?granularity={granularity}&start={start}&end={end}",
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(
        data={
            "open": [x[1] for x in data],
            "high": [x[2] for x in data],
            "low": [x[3] for x in data],
            "close": [x[4] for x in data],
            "volume": [x[5] for x in data],
        },
        index=[datetime.datetime.utcfromtimestamp(x[0]) for x in data],
    )
