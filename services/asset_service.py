# Python
from dataclasses import dataclass
# Project
from models.asset import Asset
from daos.asset_dao import AssetDao
from utils.decorators.validators import validate_class
# Externals


@validate_class(args=['asset_dao'])
@dataclass(kw_only=True)
class AssetService:
    """Class in charge of all the logic of an Asset such as validation and CRUD Operations
    """    
    asset_dao : AssetDao
    
    
    def get_asset(self, symbol) -> Asset:
        asset = self.asset_dao.get_asset(symbol)
        if self._validate(asset=asset):
            return asset
    
    
    def _validate(self, asset:Asset) -> bool:
        
        for k,v in asset.__dict__.items():
            if v is None:
                raise TypeError(f"TypeError : Not a valid data -> {k} = {v}")
            
            if isinstance(v,str):
                if len(v) == 0:
                    raise TypeError(f"TypeError : Not a valid data -> {k} = {v}")
        return True