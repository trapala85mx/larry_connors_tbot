# Python
# Project
# Externals
import talib as ta
import pandas as pd

async def rsi(src:pd.Series, period:int):
    return ta.RSI(src, period)


async def ma(src:pd.Series, period:int=200):
    return ta.MA(src, period, matype=0)


async def atr(high:pd.Series, low:pd.Series, close:pd.Series, period:int=14):
    return ta.ATR(high, low, close, period)