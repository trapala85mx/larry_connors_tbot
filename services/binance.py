# Python
# Project
from abstracts.exchange import Exchange
from utils.enums.timeframes import Timeframes
# Externals
from decouple import config
import requests as r


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
    
    
    def _create_ws(self):
        return super()._create_ws()