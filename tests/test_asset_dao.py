# Python
# Project
from daos.asset_dao import AssetDao
from utils.errors.symbol_errors import NoSymbolDataError
# Externals
import pytest


class TestAssetDao:
    
    def test_get_asset_ok(self):
        asset_dao = AssetDao()
        asset = asset_dao.get_asset("MaticUsdt")
        
        assert asset.symbol == "maticusdt" and asset.price_precision == 4 \
                and asset.qty_precision == 0 and asset.min_qty == 7 and \
                asset.min_cost == 5.02
    
    
    def test_get_asset_NoSymbolDataError(self):
        with pytest.raises(NoSymbolDataError) as e:
            asset_dao = AssetDao()
            asset_data = asset_dao.get_asset("adausdt")
            
        assert "NoSymbolDataError" in str(e.value)
    
