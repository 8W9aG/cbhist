"""The function for fetching historical coinbase data."""

import datetime
import time

import pandas as pd
import tqdm

from .candles import MAX_CANDLES, fetch_candles


def fetch_historical(
    product_id: str,
    granularity: int,
    start: datetime.datetime,
    end: datetime.datetime | None = None,
) -> pd.DataFrame:
    """Fetch the historical candles for a product."""
    if end is None:
        end = datetime.datetime.now()

    # Setup index
    start_ts = int(time.mktime(start.timetuple()))
    end_ts = int(time.mktime(end.timetuple()))
    times = list(range(start_ts, end_ts, granularity * MAX_CANDLES))
    dfs: list[pd.DataFrame | None] = [None for _ in range(len(times))]

    # Find starting time
    while True:
        last_empty_idx = 0
        for df in dfs:
            if df is None or not df.empty:
                break
            last_empty_idx += 1
        first_nonempty_idx = 0
        for df in dfs:
            if df is not None and not df.empty:
                break
            first_nonempty_idx += 1
        if abs(last_empty_idx - first_nonempty_idx) <= 1:
            break
        test_idx = int(last_empty_idx + ((first_nonempty_idx - last_empty_idx) / 2))
        df = fetch_candles(product_id, granularity, times[test_idx])
        dfs[test_idx] = df
        if df.empty:
            for i in range(test_idx):
                if dfs[i] is not None:
                    continue
                dfs[i] = pd.DataFrame()

    # Fill in the remainder
    for df_idx in tqdm.tqdm(range(len(dfs))):
        if dfs[df_idx] is not None:
            continue
        dfs[df_idx] = fetch_candles(product_id, granularity, times[df_idx])

    # Return the result
    return pd.concat(dfs).drop_duplicates(keep="first").sort_index(ascending=True)
