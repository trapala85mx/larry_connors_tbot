# Python
# Project
from models.asset import Asset
from utils.errors.class_errors import ArgumentsMissingError
# Externals
import pytest


class TestAsset:
    
    def test_create_asset(self):
        asset = Asset(
            symbol="MaticUsdt",
            price_precision=4,
            qty_precision=0,
            min_qty=7,
            min_cost=5.02
        )
    
        assert asset.symbol == "maticusdt" and asset.price_precision == 4 \
                and asset.qty_precision == 0 and asset.min_qty == 7 and \
                asset.min_cost == 5.02
    
    def test_create_asset_ArgumentsMissingError(self):
        with pytest.raises(ArgumentsMissingError) as e:
            asset = Asset(
                symbol="MaticUsdt",
                price_precision=4,
                qty_precision=0,
                min_qty=7,

            )
        assert "ArgumentsMissingError" in str(e.value)