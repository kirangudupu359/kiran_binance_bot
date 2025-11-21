# src/config.py

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, we just rely on environment variables
    pass

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Use testnet by default to avoid real money trading
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "true").lower() == "true"


def ensure_credentials():
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        raise RuntimeError(
            "Missing Binance credentials. "
            "Set BINANCE_API_KEY and BINANCE_API_SECRET in environment or .env file."
        )
