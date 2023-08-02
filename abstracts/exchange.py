# Python
from abc import ABCMeta
from abc import abstractmethod
# Project
from utils.enums.timeframes import Timeframes
# Externals



class Exchange(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def _base_api_endpoint(self): pass
    
    @property
    @abstractmethod
    def _kline_api_endpoint(self): pass
    
    @property
    @abstractmethod
    def _base_ws_url(self): pass
    
    @property
    @abstractmethod
    def _ws_raw_stream(self): pass
    
    @property
    @abstractmethod
    def _ws_combined_stream(self): pass
    
    @property
    @abstractmethod
    def MAX_STREAM_CONNECTION(self): pass
    
    
    @abstractmethod
    async def get_futures_klines(self, symbol:str, interval:Timeframes, limit:int = 251) -> dict: pass
    
    @abstractmethod
    async def start_kline_socket(self, symbol:str, streams:list[str], callback) -> None : pass