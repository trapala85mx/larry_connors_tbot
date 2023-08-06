# Python
import asyncio
from pprint import pprint
# Project
from abstracts.exchange import Exchange
from controllers.strategy import Strategy
from daos.asset_dao import AssetDao
from models.asset import Asset
from services.binance import Binance
from services.asset_service import AssetService
from utils.errors.symbol_errors import NoSymbolError
from utils.errors.symbol_errors import NoSymbolDataError
from utils.errors.class_errors import ArgumentsMissingError
from utils.errors.data_errors import IntegrityDataError
# External
import websockets


def ask_symbol() -> str:
    symbol = input("Ingresa la crypto a tradear -> ")
    if len(symbol) > 0:
        return symbol
    raise NoSymbolError("You must send a symbol")
    
        

# FUNCION PARA PROBAR - ESTA SE ELIMINARÁ PORQUE IRÁ EN STRATEGY
def handle_msg(msg: dict):
    print(msg)


async def main():
    # Se pregunta por el symbol
    symbol = ask_symbol()

    while True:
        try:
            # Se crean los objetos necesarios
            asset_dao : AssetDao = AssetDao()
            asset_service : AssetService = AssetService(asset_dao=asset_dao)
            asset : Asset = asset_service.get_asset(symbol=symbol)
            exchange : Exchange = Binance()
            strategy : Strategy = Strategy(asset=asset, exchange=exchange, notifier=None)

            # Iniciamos la estrategia
            await strategy.start()
            # Prueba de obtención de klines pasadas - Ok
            #data = await exchange.get_futures_klines(symbol=asset.symbol, interval="4h")

            # Prueba de recepción de datos del websocket - Ok
            #await exchange.start_kline_socket([f"{asset.symbol.lower()}@kline_1m", f"{asset.symbol.lower()}@kline_5m"], handle_msg)


        except NoSymbolDataError as e:
            print(e)
            break
        except ArgumentsMissingError as e:
            print(e)
            break
        except TypeError as e:
            print(e)
            break
        except IntegrityDataError as e:
            print(e)
            continue
        except websockets.ConnectionClosed as e:
            print(e)
            
    

    print(f"Symbol a tradear: {symbol.upper()}")


if __name__ == '__main__':
    asyncio.run(main())
