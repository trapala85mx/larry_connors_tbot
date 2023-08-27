# Python
import asyncio
from dataclasses import dataclass
from dataclasses import field
from pprint import pprint
# Project
from models.asset import Asset
from abstracts.exchange import Exchange
from abstracts.notifier import Notifier
from utils.enums.timeframes import Timeframes
from utils.indicators.talib_ind import ma
from utils.indicators.talib_ind import atr
from utils.indicators.talib_ind import rsi
from utils.errors.data_errors import IntegrityDataError
# Externals
import pandas as pd
import talib as ta


@dataclass(kw_only=True)
class Strategy:
    """Class that contains all the logic fo analyzing data, when to sell and boy and when to call the notifier
    Raises:
        IntegrityDataError: When data is not continous
    """    
    asset : Asset
    exchange : Exchange
    notifier : Notifier
    streams_list : list[str] = field(default_factory=list, init=False)
    snapshot : pd.DataFrame = field(default=None, init=False)
    signal_sent : bool = field(default=False, init=False)
    
    
    def __post_init__(self):
        self.streams_list.append(f"{self.asset.symbol}@kline_{Timeframes.TIMEFRAME_4HOUR.value}")
        #self.streams_list.append(f"{self.asset.symbol}@kline_{Timeframes.TIMEFRAME_1minute.value}")
    
    
    async def _get_snapshot(self, interval: Timeframes, limit:int=500) -> None:
        """Get the las "limi" klines in the exchange for analysis

        Args:
            interval (Timeframes): Enum that represent a timframe in this cases is 4 hours for this strategy
            limit (int, optional): How many candles will retrieve from the exchange
        """        
        klines = await self.exchange.get_futures_klines(self.asset.symbol, interval, limit)
        df = pd.DataFrame(klines)
        df = df.iloc[:len(klines)-1,:6]
        df.columns = ["open_time", "open", "high", "low", "close", "volume"]
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["open"] = df["open"].astype("float64")
        df["high"] = df["high"].astype("float64")
        df["low"] = df["low"].astype("float64")
        df["close"] = df["close"].astype("float64")
        df["volume"] = df["volume"].astype("float64")
        self.snapshot = df
    
    '''
    Lo que se recibe del websocket
    {
      "e": "kline",     // Event type
      "E": 1638747660000,   // Event time
      "s": "BTCUSDT",    // Symbol
      "k": {
        "t": 1638747660000, // Kline start time
        "T": 1638747719999, // Kline close time
        "s": "BTCUSDT",  // Symbol
        "i": "1m",      // Interval
        "f": 100,       // First trade ID
        "L": 200,       // Last trade ID
        "o": "0.0010",  // Open price
        "c": "0.0020",  // Close price
        "h": "0.0025",  // High price
        "l": "0.0015",  // Low price
        "v": "1000",    // Base asset volume
        "n": 100,       // Number of trades
        "x": false,     // Is this kline closed?
        "q": "1.0000",  // Quote asset volume
        "V": "500",     // Taker buy base asset volume
        "Q": "0.500",   // Taker buy quote asset volume
        "B": "123456"   // Ignore
      }
    }
    '''
    async def _update_snapshot(self, candle_df:pd.DataFrame):
        """Update snapshot with last close kline obtained from websocket

        Args:
            candle_df (pd.DataFrame): Ls Kline closed

        Raises:
            IntegrityDataError: When timdelta is different from 4
        """        
        # Revisamos que tengamos la diferencia entre velas adecuada al timeframe
        dif = (candle_df['open_time'].iloc[0] - self.snapshot['open_time'].tail(1).iloc[0]).total_seconds() / (1*60*60)
        
        if dif == 4:
            self.snapshot = pd.concat([self.snapshot, candle_df], ignore_index=True)
            await self._get_indicators()
            return
        
        raise IntegrityDataError(f"Candles aren't consecutive for {self.asset.symbol.upper()}")

    
    async def _get_indicators(self) -> None:
        """Calculate all the indicators neceesary for the strategy
        """        
        tasks = []
        tasks.append(asyncio.create_task(ma(self.snapshot.close, 11)))
        tasks.append(asyncio.create_task(ma(self.snapshot.close, 265)))
        tasks.append(asyncio.create_task(atr(self.snapshot.high, self.snapshot.low, self.snapshot.close, 14)))
        tasks.append(asyncio.create_task(rsi(self.snapshot.close, 2)))
        
        ma11, ma265, atr14, rsi2 = await asyncio.gather(*tasks)
        
        self.snapshot["ma11"] = round(ma11, self.asset.price_precision)
        self.snapshot["ma265"] = round(ma265, self.asset.price_precision)
        self.snapshot["atr14"] = round(atr14, self.asset.price_precision)
        self.snapshot["rsi2"] = round(rsi2,2)
    
    
    async def _process_kline_data(self, msg:dict) -> None:
        """Process the data from websocket

        Args:
            msg (dict): data from websocket
        """        
        if msg.get("stream"):
            candle_closed = msg.get('data', {}).get('k',{}).get('x', False)
            
            if candle_closed:
                candle_data = msg.get('data', {}).get('k',{})
                # Convertimos en DataFrame el Candle
                candle = {
                    'open_time': candle_data["t"],
                    'open':candle_data["o"],
                    'high':candle_data["h"],
                    'low':candle_data["l"],
                    'close':candle_data["c"],
                    'volume':candle_data["l"]
                }
                candle_df = pd.DataFrame([candle])
                candle_df["open_time"] = pd.to_datetime(candle_df["open_time"], unit="ms")
                candle_df["open_time"] = pd.to_datetime(candle_df["open_time"], unit="ms")
                candle_df["open"] = candle_df["open"].astype("float64")
                candle_df["high"] = candle_df["high"].astype("float64")
                candle_df["low"] = candle_df["low"].astype("float64")
                candle_df["close"] = candle_df["close"].astype("float64")
                candle_df["volume"] = candle_df["volume"].astype("float64")
                await self._update_snapshot(candle_df)
                await self._analyze()   
                

    async def _logica_señal_experimental(self):
        last_close = self.snapshot.tail(1)["close"].iloc[0]
        previous_rsi = self.snapshot.tail(2).head(1)["rsi2"].iloc[0]
        last_rsi = self.snapshot.tail(1)["rsi2"].iloc[0]
        last_ma11 = self.snapshot.tail(1)["ma11"].iloc[0]
        last_ma265 = self.snapshot.tail(1)["ma265"].iloc[0]
        last_atr = self.snapshot.tail(1)["atr14"].iloc[0]
        
        print("analizando")
        if last_close > last_ma265:
            if last_ma11 > last_ma265 and last_close < last_ma11:
                print(f"ma11 > ma265 and close < ma11: {last_ma11 > last_ma265 and last_close < last_ma11}")
                if last_rsi < 9:
                    print(f"rsi < 9: {last_rsi < 9}")
                    msg = {
                        "symbol" : self.asset.symbol.upper(),
                        "signal": "LONG",
                        "entrance": f"${last_close}",
                        "RSI": last_rsi
                    }
                    await self._send_singal(msg)
                    self.signal_sent = True
                    return 
        
        if last_close < last_ma265:
            print(f"close < last ma265: {last_close < last_ma265}")
            if last_ma11 < last_ma265 and last_close > last_ma11:
                print(f"close > last ma265: {last_close > last_ma265}")
                if last_rsi > 74:
                    print(f"rsi > 74: {last_rsi > 74}")
                    msg = {
                        "symbol" : self.asset.symbol.upper(),
                        "signal": "SHORT",
                        "entrance": f"${last_close}",
                        "RSI": last_rsi
                    }
                    await self._send_singal(msg)
                    self.signal_sent = True
                    return 
        self.signal_sent = False
        
        
    async def _larry_connors_logic(self):
        """Analyze data and send signal when requisites are fullfilled

        Returns:
            [dic]: msg with the data to send 
        """        
        close = self.snapshot.tail(1)["close"].iloc[0]
        rsi = self.snapshot.tail(1)["rsi2"].iloc[0]
        ma11 = self.snapshot.tail(1)["ma11"].iloc[0]
        ma265 = self.snapshot.tail(1)["ma265"].iloc[0]
        atr = self.snapshot.tail(1)["atr14"].iloc[0]
        previous_rsi = (self.snapshot.tail(2)).head(1)["rsi2"].iloc[0]
        
        # Compras
        if ma11 > ma265 and close > ma265:
            if rsi > 9 and close < ma11 and previous_rsi < 9:
                stop_loss = round(close - (atr*1.5), self.asset.price_precision)
                msg = {
                        "symbol" : self.asset.symbol.upper(),
                        "signal": "BUY - LONG",
                        "entrance": f"${close}",
                        "stop_loss": f"${stop_loss}"
                    }
                await self._send_singal(msg)
                return msg
        
        # Ventas
        if ma11 < ma265 and close < ma265:
            if rsi < 74 and close > ma11 and previous_rsi > 74:
                stop_loss = round(close + (atr*1.5), self.asset.price_precision)
                msg = {
                        "symbol" : self.asset.symbol.upper(),
                        "signal": "SELL - SHORT",
                        "entrance": f"${close}",
                        "stop_loss": f"${stop_loss}"
                    }
                await self._send_singal(msg)
                return msg
    
    
    async def _analyze(self) -> dict:
        """Analyze the data via the larry connors strategy and send signal
        """        
        # Lógica de prueba donde envía señal cuandl se cumple que RSI es menor a 9 o mayor a 74
        if not self.signal_sent:
            #await self._logica_señal_experimental() # Funciona Ok
            await self._larry_connors_logic()
        
        return
    
    
    async def _send_singal(self, msg:str) -> None:
        """Uses the notifier to send singal

        Args:
            msg (str): msg to send
        """        
        pprint(msg)
    
    
    async def start(self) -> None:
        """starts the signal bot
        """        
        #timeframe = Timeframes.TIMEFRAME_1minute.value
        timeframe = Timeframes.TIMEFRAME_4HOUR.value
        await self._get_snapshot(interval=timeframe)
        await self._get_indicators()
        # analizamos los últimos datos cerrados a ver si tenemos señal
        await self._analyze()
        # poseteriormente empezamos a recibir información
        msg = await self.exchange.start_kline_socket(self.streams_list, self._process_kline_data)
        