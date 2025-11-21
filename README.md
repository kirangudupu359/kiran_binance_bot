# Binance USDT-M Futures Order Bot

This project is a CLI-based trading bot for Binance USDT-M Futures.  
It supports **market**, **limit**, and several **advanced order types**:

- Market orders
- Limit orders
- Stop-limit orders
- OCO (take-profit + stop-loss)
- TWAP (Time-Weighted Average Price)
- Grid strategy (buy-low/sell-high in a range)

All actions are logged to `bot.log` with timestamps and error traces.

---

## 1. Project Structure

```text
[my_name]_binance_bot/
├── src/
│   ├── config.py
│   ├── utils.py
│   ├── client.py
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── advanced/
│   │   ├── __init__.py
│   │   ├── stop_limit.py
│   │   ├── oco.py
│   │   ├── twap.py
│   │   └── grid.py
│
├── bot.log
├── README.md
└── report.pdf
