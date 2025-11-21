Binance USDT-M Futures Trading Bot (Python)

This project is a CLI-based Binance USDT-M Futures trading bot built in Python.
It supports Market, Limit, and Advanced order types, including Stop-Limit, OCO, TWAP, and Grid strategies.

The goal of this project is to demonstrate:

1. Interaction with Binance USDT-M Futures API
2. Input validation
3. Logging system
4. Separation of code into modules
5. CLI execution of trading scripts

The bot is configured to use the Binance Testnet by default to ensure safety during testing.

kiran_binance_bot/
│
├── .venv/                     # Virtual environment (auto-generated)
├── .env                       # API keys (testnet/dummy for safety)
├── bot.log                    # Log file (contains bot activity)
│
├── src/
│   ├── config.py              # API keys, testnet mode, credential checks
│   ├── utils.py               # Validators + global logger
│   ├── client.py              # Binance Futures client setup
│   ├── market_orders.py       # CLI script to place MARKET orders
│   ├── limit_orders.py        # CLI script to place LIMIT orders
│   │
│   └── advanced/
│       ├── __init__.py
│       ├── stop_limit.py      # STOP-LIMIT order implementation
│       ├── oco.py             # Simulated OCO (TP + SL)
│       ├── twap.py            # TWAP strategy
│       └── grid.py            # GRID strategy
│
├── README.md                  # Project documentation
└── report.pdf                 # Assignment explanation + screenshots

Requirements:

1. Python 3.9+
2. Binance Testnet API Key and Secret
3. Modules (install with pip):
pip install python-binance python-dotenv numpy


Environment Variables (.env file)

Create a .env file in the project root:
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true

How to Run the Bot

All scripts are run through CLI.
Open terminal inside the project folder and activate your virtual environment:
.\.venv\Scripts\activate

Then run scripts like this:

 1. Market Order
python src/market_orders.py BTCUSDT BUY 0.001


Example output:

Error placing market order. Check bot.log for details.


(As i used dummy keys it has arrived like this)

 2. Limit Order
python src/limit_orders.py BTCUSDT SELL 0.001 65000

 Advanced Order Types
 Stop-Limit Order
python src/advanced/stop_limit.py BTCUSDT BUY 0.001 65000 64950

 OCO (One-Cancels-Other)
python src/advanced/oco.py BTCUSDT SELL 0.001 70000 65000 64800

 TWAP Strategy
python src/advanced/twap.py BTCUSDT BUY 0.1 5 10


This buys 0.1 BTC in 5 slices, 10 seconds apart.

 Grid Strategy
python src/advanced/grid.py BTCUSDT BUY 0.05 60000 70000 5


Places BUY limit orders between 60k → 70k at 5 evenly spaced levels.

 Logging System

All activity is logged inside:

bot.log


Each entry follows this structure:

YYYY-MM-DD HH:MM:SS | module_name | LEVEL | message


Example (test log):

2025-11-21 14:45:10 | test | INFO | test log entry


