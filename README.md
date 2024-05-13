# cbhist

<a href="https://pypi.org/project/cbhist/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/cbhist">
</a>

A python library for pulling in historical candles from coinbase.

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [tqdm](https://github.com/tqdm/tqdm)
- [tenacity](https://tenacity.readthedocs.io/en/latest/)

## Raison D'être :thought_balloon:

The [coinbase exchange API](https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles) lets you pull down historical OHLC data but only 300 candles at a time. If you are trying to get data at the minute resolution this can take a long time. Typically the approach is to iterate across a time series and perform a request for each time chunk, however this can be sped up greatly by doing a binary search before doing an iterative pull to determine when the asset begins to have candles. Formalising this into a proper library produces a dataframe made it easier to work in different projects than re-inventing the wheel each time.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install cbhist`

## Usage example :eyes:

To pull a dataframe containing all the candles for a coinbase product:

```python
import datetime

from cbhist.historical import fetch_historical

granularity = 60 # Candle for every minute
df = fetch_coinbase("ETH-USD", granularity, datetime.datetime(2010, 1, 1))
```

This results in a dataframe with a datetime index and OHLC (+ volume) columns.

## License :memo:

The project is available under the [MIT License](LICENSE).
