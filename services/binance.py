# Python
import json
import asyncio
from typing import List
# Project
from abstracts.exchange import Exchange
from utils.enums.timeframes import Timeframes
# Externals
from decouple import config
import requests as r
import websockets


class Binance(Exchange):
    
    NAME = "BINANCE"
    
    def __init__(self) -> None:
        super().__init__()
    
    @property  
    def _base_api_endpoint(self):
        return config(f"{self.NAME}_BASE_API_ENDPOINT")
    
    @property
    def _kline_api_endpoint(self):
        return config(f"{self.NAME}_KLINE_API_ENDPOINT")
    
    @property
    def _base_ws_url(self):
        return config(f"{self.NAME}_WEBSOCKET_BASE_URL")
    
    @property
    def _ws_raw_stream(self):
        return config(f"{self.NAME}_WEBSCOKET_RAW_STREAM")
    
    @property
    def _ws_combined_stream(self):
        return config(f"{self.NAME}_WEBSCOKET_COMBINED_STREAM")
    
    @property
    def MAX_STREAM_CONNECTION(self):
        return config(f"{self.NAME}_MAX_STREAM_CONNECTIONS")
    
    @property
    def _ws(self):
        return None
    
    @_ws.setter
    def _ws(self, ws):
        pass
    
    async def get_futures_klines(self, symbol:str, interval:Timeframes, limit:int = 251) -> dict:
        try:
            params = {
                'symbol': symbol.lower(),
                'interval': interval,
                'limit' : limit
            }
            
            url = f"{self._base_api_endpoint}{self._kline_api_endpoint}"
            
            response = r.get(url, params=params)
            response.raise_for_status()
            return response.json()
        
        except r.exceptions.RequestException as e:
            print(f"HTTP error while get_futures_kline for {symbol.upper()}:\n{e}")
        
        except Exception as e:
            print(f"Unexpected error in get_futures_klines for {symbol.upper()}:\n{e}")
        
    
    # suscripción a los klines
    async def _subscribe(self, ws, streams:List[str]) -> None:
        payload = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id":1
        }

        await ws.send(json.dumps(payload))
    
    # Iniciar websocket
    async def start_kline_socket(self, streams:List[str], callback) -> None:
        if len(streams) < int(self.MAX_STREAM_CONNECTION):
            async for websocket in websockets.connect(self._base_ws_url+self._ws_combined_stream):
                    await self._subscribe(websocket, streams)
                    async for message in websocket:
                        await callback(json.loads(message))
                    
        raise ValueError("Too many streams")
    