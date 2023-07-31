# Python
import asyncio
# Project
from app import ask_symbol
from utils.errors.symbol_errors import NoSymbolError
# External
import pytest
#@pytest.mark.trio -> decorador para funciones/metodos asíncronos

class TestApp:
    
    def test_ask_symbol(self, mocker):
        mocker.patch('builtins.input', return_value="maticusdt")
        symbol = ask_symbol()
        assert len(symbol) > 0
    
    def test_raise_NoSymbolError(self, mocker):
        with pytest.raises(NoSymbolError) as e:
            mocker.patch('builtins.input', return_value="")
            symbol = ask_symbol()
            assert "NoSymbolError" in str(e.value)