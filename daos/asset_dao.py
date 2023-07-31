# Python
from dataclasses import dataclass
from data.example_data import data
from models.asset import Asset
from utils.errors.symbol_errors import NoSymbolDataError
# Project
# Externals


@dataclass
class AssetDao:
    
    def get_asset(self, symbol:str):
        asset_data = data.get(symbol.lower(), None)
        
        if asset_data is None:
            raise NoSymbolDataError(symbol,"No data for the crypto")
        asset = Asset(
            symbol=symbol.lower(),
            price_precision=asset_data["price_precision"],
            qty_precision=asset_data["qty_precision"],
            min_qty=asset_data["min_qty"],
            min_cost=asset_data["min_cost"]
        )
        
        return asset