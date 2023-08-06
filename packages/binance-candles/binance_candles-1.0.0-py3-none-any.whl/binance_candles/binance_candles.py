import time
import logging
import datetime
from decimal import Decimal
from binance import ThreadedWebsocketManager
from threading import Lock

class Candle:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price_open_dt = None
        self.price_close_dt = None
        self.price_open = None
        self.price_close = None
        self.price_low = None
        self.price_high = None

    def update(self, price_dt, price):
        self.price_close_dt = price_dt
        self.price_close = price

        if self.price_open_dt is None:
            self.price_open = self.price_low = self.price_high = price
            self.price_open_dt = price_dt

        if price < self.price_low:
            self.price_low = price
        if price > self.price_high:
            self.price_high = price

    def generate_next(self):
        candle = Candle(self.symbol)
        candle.price_open = candle.price_low = candle.price_high = candle.price_close = self.price_close
        candle.price_open_dt = candle.price_close_dt = self.price_close_dt
        return candle

    def copy(self):
        candle = Candle(self.symbol)
        candle.price_open_dt = self.price_open_dt
        candle.price_close_dt = self.price_close_dt
        candle.price_open = self.price_open
        candle.price_low = self.price_low
        candle.price_high = self.price_high
        candle.price_close = self.price_close
        return candle

    def __str__(self):
        return f"{str(self.price_open_dt)}-{str(self.price_close_dt)} {self.symbol} {self.price_open} {self.price_low} {self.price_high} {self.price_close}"


def candles_generator(symbols=None, interval=60):
    active_candles = {}
    active_candles_lock = Lock()

    def price_handler(symbols, msg):
        if "e" in msg:
            logging.error(msg["m"])
            return
        data = msg["data"]
        with active_candles_lock:
            if type(data) is dict:
                data = [data]
            for entry in data:
                symbol = entry["s"]
                if symbols is not None:
                    if type(symbols) == str:
                        symbols = [symbols]
                    if symbol not in symbols:
                        return
                price_dt = datetime.datetime.fromtimestamp(entry["E"] / 1000)
                price = Decimal(entry["i"]) if "i" in entry else (Decimal(entry["a"]) + Decimal(entry["b"])) / 2
                if symbol not in active_candles:
                    candle = Candle(symbol)
                    active_candles[symbol] = candle
                else:
                    candle = active_candles[symbol]
                candle.update(price_dt, price)

    def reset_candles(active_candles):
        with active_candles_lock:
            completed_candles = list(active_candles.values())
            for candle in completed_candles:
                active_candles[candle.symbol] = candle.generate_next()
            return completed_candles

    twm = ThreadedWebsocketManager()
    twm.start()
    twm.start_all_mark_price_socket(lambda msg: price_handler(symbols, msg))
    while True:
        time.sleep(interval)
        yield reset_candles(active_candles)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    for candles in candles_generator(symbols=["BTCUSDT"], interval=60):
        print(",".join(map(str, candles)))
