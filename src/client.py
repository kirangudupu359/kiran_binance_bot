# src/client.py

from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_TESTNET, ensure_credentials
from utils import get_logger

logger = get_logger("client")


def get_futures_client() -> Client:
    """Create a Binance Futures client (testnet by default)."""
    ensure_credentials()

    client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

    if BINANCE_TESTNET:
        # Point the futures endpoints to testnet
        # This pattern is commonly used with python-binance for futures testnet.
        client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        logger.info("Using Binance Futures TESTNET.")
    else:
        logger.info("Using Binance Futures MAINNET (real money).")

    return client
