# Python
from abc import ABCMeta
from abc import abstractmethod
# Project
from utils.enums.timeframes import Timeframes
# Externals



class Exchange(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def base_api_endpoint(self): pass
    
    
    @property
    @abstractmethod
    def kline_api_endpoint(self): pass
    
    
    @property
    @abstractmethod
    def base_ws_url(self): pass
    
    
    @property
    @abstractmethod
    def ws_raw_stream(self): pass
    
    
    @property
    @abstractmethod
    def ws_combined_stream(self): pass
    
    
    @abstractmethod
    def get_futures_klines(self, symbol:str, interval:Timeframes, limit:int = 251) -> dict: pass
    
    @abstractmethod
    def futures_kline_socket(self, symbol:str, interval:Timeframes) -> None : pass
    
    @abstractmethod
    def _create_ws(self)