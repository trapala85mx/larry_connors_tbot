# Python
from dataclasses import dataclass
# Project
from utils.decorators.validators import validate_class
# Externals

@validate_class(args=["symbol", "price_precision", "qty_precision", "min_qty", "min_cost"])
@dataclass(kw_only=True)
class Asset:
    symbol : str
    price_precision : int
    qty_precision : int
    min_qty : float
    min_cost : float
    
    
    def __post_init__(self):
        self.symbol = self.symbol.lower()
        
        
    def __str__(self) -> str:
        return f"Symbol: {self.symbol.upper()}"