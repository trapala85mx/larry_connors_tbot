# Python
import asyncio
# Project
from daos.asset_dao import AssetDao
from services.asset_service import AssetService
from services.binance import Binance
from abstracts.exchange import Exchange
from utils.errors.symbol_errors import NoSymbolError
from utils.errors.symbol_errors import NoSymbolDataError
from utils.errors.class_errors import ArgumentsMissingError
# External
from pprint import pprint

def ask_symbol() -> str:
    while True:
        try:
            symbol = input("Ingresa la crypto a tradear -> ")
            if len(symbol) > 0:
                return symbol
            raise NoSymbolError("You must send a symbol")
        except NoSymbolError as e:
            print(e)
            continue

# FUNCION PARA PROBAR - ESTA SE ELIMINARÁ PORQUE IRÁ EN STRATEGY
def handle_msg(msg: dict):
    print(msg)


async def main():
    # Se pregunta por el symbol
    symbol = ask_symbol()

    # Se crean los objetos necesarios
    try:
        asset_dao = AssetDao()
        asset_service = AssetService(asset_dao=asset_dao)
        asset = asset_service.get_asset(symbol=symbol)
        exchange : Exchange = Binance()
        #data = await exchange.get_futures_klines(symbol=asset.symbol, interval="4h")
        
        await exchange.start_kline_socket([f"{asset.symbol.lower()}@kline_1m", f"{asset.symbol.lower()}@kline_5m"], handle_msg)
        
        
    except NoSymbolDataError as e:
        print(e)
    except ArgumentsMissingError as e:
        print(e)
    except TypeError as e:
        print(e)
    

    print(f"Symbol a tradear: {symbol.upper()}")


if __name__ == '__main__':
    asyncio.run(main())
