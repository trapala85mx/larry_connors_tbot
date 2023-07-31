class NoSymbolError(Exception):
    
    def __init__(self, msg:str) -> None:
        self._msg = msg
    
    def __str__(self):
        return f"NoSymbolError : {self._msg}"


class NoSymbolDataError(Exception):
    
    def __init__(self, symbol:str, msg:str) -> None:
        self._symbol = symbol
        self._msg = msg
    
    def __str__(self):
        return f"NoSymbolDataError for {self._symbol.upper()}: {self._msg}"