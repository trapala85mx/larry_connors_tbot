# Python
# Project
from app import ask_symbol
from models.asset import Asset
from daos.asset_dao import AssetDao
from services.asset_service import AssetService
from utils.errors.class_errors import ArgumentsMissingError
# Externals
import pytest


class TestAssetService:
    
    def test_create_asset_service_ok(self):
        asset_dao = AssetDao()
        asset_service = AssetService(asset_dao=asset_dao)
        
        assert isinstance(asset_dao,AssetDao)
    
    
    def test_create_asset_ArgumentsMissingError(self):
        with pytest.raises(ArgumentsMissingError) as e:
            asset_dao = AssetDao()
            asset_service = AssetService()
        
        assert "ArgumentsMissingError" in str(e.value)
    
    
    def test_get_asset_ok(self, mocker):
        mocker.patch('builtins.input', return_value="maticusdt")
        symbol = ask_symbol()
        asset_dao : AssetDao = AssetDao()
        asset_service : AssetService = AssetService(asset_dao=asset_dao)
        asset : Asset = asset_service.get_asset(symbol)
    
    
    def test_validate_false(self, mocker):
        with pytest.raises(TypeError) as e:
            mocker.patch('builtins.input', return_value="coin1")
            symbol = ask_symbol()
            asset_dao : AssetDao = AssetDao()
            asset_service : AssetService = AssetService(asset_dao=asset_dao)
            asset : Asset = asset_service.get_asset(symbol)
            asset_service._validate(asset)
        assert "TypeError" in str(e.value)