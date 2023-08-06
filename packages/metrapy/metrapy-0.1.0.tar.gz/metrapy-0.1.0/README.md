# metrapy
A batteries included wrapper around MetaTrader5's python utility.

[+] Wrapper Functions: Get account, tickers, orders, positions, history & deals

[+] Polling utility that uses thread to fetch data periodically

[+] Wrapper utility for placing orders, Maps for MT5 constants

## What does it tries to solve?
It tries to make working with Python + MT5 easier, by adding default validation & error messages, parsing responses, and wrapping them appropriately. 

## Installation
```python
  pip install metrapy
```

## Connection

```py
  from metrapy.connector import MT5

  mpy = MT5({
    'server': 'ServerName-Global',
    'login': 1876876,
    'password': 'yourpass'
  })

  # Default terminal path location is already provided. However, you can override that with your own.

   mpy = MT5({
    'path': 'your-terminal-location',
    'server': 'ServerName-Global',
    'login': 1876876,
    'password': 'yourpass'
  })
```
[x] Make sure you have Algorithmic trading enabled in MT5 terminal

### Exposed Defaults

- `timezone` is UTC 0 by default, you can override it with your own.
- `mt5` core package is exposed as `_mt5` property. so, you do not need to import it explicitly.

```py
   mt5 = mpy._mt5
```

- All the mappings are exposed via `mpy.maps` property.
- `mpy.connected` provides connected status
- You can pass `magic` & `debug` parameters to the MT5() constructor, for helpful debugging. 

## Polling Utility
MT5 does not provide for data fetching in realtime mode. So, the options are 
1. Poll your data, on regular time intervals
2. Make a bridge between MQL5 & Python to fetch that data (using sockets, streams or something else)

Support for 1 is available and should be useful enough in most of the cases.

```py
  from metrapy.sync import poller

  poller(your_func, timeframe, adjusted_secs=0)
```

- your_func is piece of code to execute at any given timeframe
- supports integer (number of secs), or timeframe (1s, 1M, 2M, 5M, 15M, 30M, 1H, 4H, 1D, 1W)

```py

   def start():
     print("5 minutes spent")

    poller(start, "5M")

    poller(start, 100, 2)

```

It must be noted that code will run at regular time intervals, not from when you start the code. For example, above code will run at HH:05, HH:10, HH:15, HH:20, ...

