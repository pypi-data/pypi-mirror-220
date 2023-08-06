from metrapy.sync import get_current_time
from metrapy.maps import (
    mt5tf_map,
    order_types_map,
    position_type,
    filling_type,
    time_type,
)

from metrapy.defaults import defaults
from metrapy.utils import get_candles_df, filter_props

import MetaTrader5 as mt5
import pandas as pd
import uuid

import logging

class MT5:
    _mt5 = mt5
    magic: None
    timezone = defaults.timezone
    connected = False
    debug = False
    maps = {
        'timeframe': mt5tf_map,
        'order': order_types_map,
        'position': position_type,
        'filling': filling_type,
        'time': time_type
    }

    def __init__(self, params, opts={}):
        if "login" not in params:
            raise Exception("Please provide MT5 login.")

        if "pass" not in params:
            raise Exception("Please provide MT5 password.")

        if "server" not in params:
            raise Exception("MT5 Server Name is missing. Please provide.")

        if "path" not in params:
            print(
                "MT5 binary (terminal) installation path is mising. \n Using Default: C:/Program Files/MetaTrader 5/terminal64.exe"
            )

        if type(params["login"]) != int:
            raise Exception("login parameter must be a number")

        self.connected = mt5.initialize(
            path=params["path"] if "path" in params else defaults.mt5_path,
            server=params["server"],
            login=params["login"],
            password=params["pass"],
        )

        if not self.connected:
            print("Error while trying to connect to MT5")
            print(params)
            quit()

        if "timezone" in opts:
            self.timezone = opts["timezone"]

        if "debug" in opts:
            self.debug = True

        if "magic" in params:
            self.magic = params['magic_id']

    def get_account_info(self):
        return mt5.account_info()._asdict()

    def get_tickers(self, params={}):
        if "ticker" in params:
            return mt5.symbol_info(params["ticker"])

        if "group" in params:
            return mt5.symbols_get(group=params["group"])

        symbols = mt5.symbols_get()
        tickers = []

        for sym in symbols:
            if "filter_props" in params:
                tickers.append(filter_props(sym._asdict(), params["filter_props"]))
                continue

            tickers.append(sym._asdict())

        return tickers

    def get_tickers_count(self, params={}):
        if "group" in params:
            return mt5.symbols_get(group=params["group"])

        return mt5.symbols_total()

    def get_candles(self, params):
        if "ticker" not in params:
            raise Exception("Please provide ticker information")

        if "timeframe" not in params:
            raise Exception(
                "Please provide timeframe for which candles are to be fetched"
            )

        if "count" not in params:
            raise Exception("Please provide count of candles to be fetched.")

        candles = mt5.copy_rates_from_pos(
            params["ticker"],
            mt5tf_map[params["timeframe"]],
            params["start"] if "start" in params else 0,
            params["count"],
        )

        if candles is None:
            return {
                "candles": None,
                "last_error": mt5.last_error(),
                "params": params,
            }

        if self.debug:
            print(
                "Candles Fetched: ",
                params["ticker"],
                get_current_time().strftime("%m/%d/%Y, %H:%M:%S", len(candles)),
            )

        candles_df = get_candles_df(candles, timezone= params['timezone'] if "timezone" in params else None)

        return {"candles": candles, "last_error": None, "params": params, 'candles_df': candles_df}

    def get_last_candle(self, params):
        if "ticker" not in params:
                raise Exception("Please provide ticker information")
        
        if "timeframe" not in params:
                raise Exception(
                    "Please provide timeframe for which candles are to be fetched"
                )
        
        candle_raw = mt5.copy_rates_from_pos(
                params["ticker"],
                mt5tf_map[params["timeframe"]],
                0,
                1,
            )
        
        if candle_raw is None:
                return {
                    "candle": None,
                    "last_error": mt5.last_error(),
                    "params": params,
                }
        
        if self.debug:
                print(
                    "Candles Fetched: ",
                    params["ticker"],
                    get_current_time().strftime("%m/%d/%Y, %H:%M:%S", len(candle_raw)),
                )
        
        candle = get_candles_df(candle_raw, timezone= params['timezone'] if "timezone" in params else None)
        
        return {"candle_raw": candle[0] if len(candle) > 0 else None, "last_error": None, "params": params, 'candles_df': candle.iloc[0] if candle else None}

    def get_orders(self, params):
        request = {}

        if "ticker" in params:
            request["symbol"] = params["ticker"]

        if "ticket" in params:
            request["ticket"] = params["ticket"]

        if "group" in params:
            request["group"] = params["group"]

        orders = mt5.orders_get(**request)

        if orders is None:
            return {
                'orders': None,
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }
        
        orders_list = []

        for o in orders:
            orders_list.append(o._asdict())

        return {
            'orders': orders_list,
            'count': len(orders_list),
            'last_error': None,
            'params': params,
            '_request': request
        }

    def get_positions(self, params):
        request = {}

        if "ticker" in params:
            request["symbol"] = params["ticker"]

        if "ticket" in params:
            request["ticket"] = params["ticket"]

        if "group" in params:
            request["group"] = params["group"]

        positions = mt5.positions_get(**request)

        if positions is None:
            return {
                'orders': None,
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }
        
        pos_list = []

        for pos in positions:
            pos_list.append(pos._asdict())

        return {
            'positions': pos_list,
            'count': len(pos_list),
            'last_error': None,
            'params': params,
            '_request': request
        }

    def get_history(self, params):

        request = {}
        
        if 'ticket' in params:
            ticket = params["ticket"]

            if type(ticket) != int:
                raise Exception("ticket parameter should be an integer.")

            request['ticket'] = ticket

        if "position" in params:

            pos = params["position"]

            if type(pos) != int:
                raise Exception("position parameter should be an integer.")

            request['position'] = pos

        if "start" in params:
            request["date_from"] = params["start"]

        if "end" in  params:
            request["date_to"] = params["end"]

        if "group" in params:
            request["group"] = params["group"]

        orders = mt5.history_orders_get(**request)

        if orders is None:
            return {
                'orders': None,
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }
        
        orders_list = []

        for o in orders:
            orders_list.append(o._asdict())

        return {
            'orders': orders_list,
            'count': len(orders_list),
            'last_error': None,
            'params': params,
            '_request': request
        }
    
    def get_history_deals(self, params):

        request = {}
        
        if 'ticket' in params:
            ticket = params["ticket"]

            if type(ticket) != int:
                raise Exception("ticket parameter should be an integer.")

            request['ticket'] = ticket

        if "position" in params:

            pos = params["position"]

            if type(pos) != int:
                raise Exception("position parameter should be an integer.")

            request['position'] = pos

        if "start" in params:
            request["date_from"] = params["start"]

        if "end" in  params:
            request["date_to"] = params["end"]

        if "group" in params:
            request["group"] = params["group"]

        deals = mt5.history_deals_get(**request)

        if deals is None:
            return {
                'deals': None,
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }
        
        deals_list = []

        for deal in deals:
            deals_list.append(deal._asdict())

        return {
            'orders': deals_list,
            'count': len(deals_list),
            'last_error': None,
            'params': params,
            '_request': request
        }

    def place_order(self, params):
        id = uuid.uuid4().int & (1 << 64) - 1

        def get_order_type():
            type = params["order_type"]

            if params["trade_type"] == "short":
                type = type + "_SELL"

            if params["trade_type"] == "long":
                type = type + "_BUY"

            if "stop_order" in params and params["stop_order"]:
                type = type + "_STOP"

            if "stop_limit_order" in params and params["stop_limit_order"]:
                type = type + "_STOP_LIMIT"

            return type

        request = {
            "magic": self.magic,
            "symbol": params["ticker"],
            "action": order_types_map[params["order_type"]],
        }

        if "trade_type" in params:
            request["type"] = position_type[get_order_type()]

        if "filling_type" in params:
            request["type_filling"] = filling_type[params["filling_type"]]

        if "time_type" in params:
            request["type_time"] = filling_type[params["time_type"]]

        if "price" in params:
            request["price"] = params["price"]

        if "lots" in params:
            request["volume"] = float(params["lots"])

        if "stoploss" in params:
            request["sl"] = params["stoploss"]

        if "takeprofit" in params:
            request["tp"] = params["takeprofit"]

        if "ticket" in params:
            request["order"] = params["ticket"]

        if "position" in params:
            request["position"] = params["position"]

        if "expire_time" in params:
            request["expiration"] = params["expire_time"]

        if "deviation" in params:
            request["deviation"] = params["deviation"]

        result = mt5.order_send(request)

        if result is None:

            if self.debug:
                print("[Log`]: Unable to add order, check provided parameters")
                print("Request:", pd.Series(request))

            return {
                'magic_id': self.magic,
                'identifier': id,
                'result': None,
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }

        result = result._asdict()

        if result["retcode"] == 10019:

            if self.debug:
                logging.warn(f"Code [{result['retcode']}]: {result['comment']}")
                logging.warn(
                    "Unable to place order. Close some positions or add some funds"
                )

            return {
                'magic_id': self.magic,
                'identifier': id,
                'result': result,
                'error_info': '[10019]: Close some positions or add funds.',
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }

        if result["retcode"] != 10009:

            if self.debug:
                logging.info(
                    f"Code [{result['retcode']}]: Error while placing Order. Please try again."
                )
                logging.debug(f"\n Request \n:  {pd.Series(request)}")
                logging.debug(f"\n Response \n:  {pd.Series(result)}")

            return {
                'magic_id': self.magic,
                'identifier': id,
                'result': result,
                'error_info': 'Check last error or result.',
                'last_error': mt5.last_error(),
                'params': params,
                '_request': request
            }

        return {
            "magic_id": self.magic,
            "identifier": id,
            "result": result,
            'error_info': None,
            'last_error': None,
            'params': params,
            '_request': request
        }
