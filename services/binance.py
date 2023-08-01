# Python
# Project
from abstracts.exchange import Exchange
from utils.enums.timeframes import Timeframes
# Externals
from decouple import config
import requests as r


class Binance(Exchange):
    
    
    def __init__(self) -> None:
        super().__init__()
        self._base_api_endpoint = config("BINANCE_BASE_API_ENDPOINT") 
        self._kline_api_endpoint = config("BINANCE_KLINE_API_ENDPOINT")
        self._base_ws_url = config("BINANCE_WEBSOCKET_BASE_URL")
        self._ws_raw_stream = config("BINANCE_WEBSCOKET_RAW_STREAM")
        self._ws_combined_stream = config("BINANCE_WEBSCOKET_COMBINED_STREAM")
        
    @property
    def base_api_endpoint(self): return self._base_api_endpoint
    
    
    @property
    def kline_api_endpoint(self): return self._kline_api_endpoint
    
    
    @property
    def base_ws_url(self): return self._base_ws_url
    
    
    @property
    def ws_raw_stream(self): return self._ws_raw_stream
    
    
    @property
    def ws_combined_stream(self): return self._ws_combined_stream
    

    
    def get_futures_klines(self, symbol:str, interval:Timeframes, limit:int = 251) -> dict:
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
        
        

    def futures_kline_socket(self, symbol:str, interval:Timeframes) -> None:
        pass