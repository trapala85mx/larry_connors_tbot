# Summary

This is a script for trading signal in crypto using Larry Connors Strategy with some changes


# To consider
I didn't finish this script because i got a better idea to create a trading bot taht noly needs to create strategies, so i decided to "kill" this script and create a new one called trading_bot

This script was started using TDD (Test Driven Development) Methhodology and it works and send signal but you need to add the data necessary inside data/example_data.py

# Pre requisites
- Python 3.10 
- Talib wheel Installed<br>
You can go either https://trapalamx.notion.site/Ta-Lib-b048ef6dfddc454cb579fbccc1e6a1cb?pvs=4 or https://github.com/ta-lib/ta-lib-python to check how to install in Linux / WSL2. For windows install check the github page


# Execute (LINUX / WSL2)


1. Clone repository
```shell
# SSH
git clone git@github.com:trapala85mx/larry_connors_tbot.git
# HTTPS
git clone https://github.com/trapala85mx/larry_connors_tbot.git
```


2. Move to the folder
```shell
cd larry_connors_tbot
```


3. Create virtual environment. In my case y create an alias into my ~/.zshrc for this and reestasrt shell

```shell
# If you create alias, insert into .zshrc / .bahrc file
alias py310='python3.10 -m venv env'
# After Alias
source ~/.zshrc
```
```shell
# Virtual Env
py310
```


4. Activante Virtualenv
```shell
source env/bin/activate
```

5. Install requirements.txt
```shell
pip install -r requirements.txt
```
6. Create a .env file and fill with this:
```shell
BINANCE_BASE_API_ENDPOINT = "https://fapi.binance.com"
BINANCE_KLINE_API_ENDPOINT = "/fapi/v1/klines"
BINANCE_WEBSOCKET_BASE_URL = "wss://fstream.binance.com"
BINANCE_WEBSCOKET_RAW_STREAM = "/ws/"
BINANCE_WEBSCOKET_COMBINED_STREAM = "/stream"
BINANCE_MAX_STREAM_CONNECTIONS = 200
```
7. Execute
```shell
python app.py
```


# How to use
Once you execute, it will ask for a symbol in Binance Futures
You need to write a crypot with usdt at the end
so, for example:
```shell
# Execute
python main.py
# OUTPUT
Ingresa la crypto a tradear -> maticusdt
```

Then, you only need to wait to message in console appears gibing you the data

| NOTE: This mod is using a stop loss that i dont 
recommend , i prefer to follow Larrry Connors and close position whe close price breaks ma11. This is bacuse losses are greater with SL

