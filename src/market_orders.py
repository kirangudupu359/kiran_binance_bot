# src/market_orders.py

import argparse
import datetime

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    ValidationError,
)

logger = get_logger("market_orders")


def write_log_line(message: str) -> None:
    """
    Fallback manual logger that always appends to bot.log.
    This guarantees that the assignment log file is not empty,
    even if the logging module behaves differently on some systems.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | market_orders | {message}\n"
    with open("bot.log", "a", encoding="utf-8") as f:
        f.write(line)


def place_market_order(symbol: str, side: str, quantity: float):
    client = get_futures_client()

    msg = f"Sending MARKET order: {side} {quantity} {symbol}"
    logger.info(msg)
    write_log_line(msg)

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )

        msg_ok = f"MARKET order placed successfully. OrderId={order.get('orderId')}"
        logger.info(msg_ok)
        write_log_line(msg_ok)

        return order

    except Exception as exc:
        err_msg = f"Failed to place MARKET order: {exc}"
        logger.exception(err_msg)
        write_log_line(err_msg)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Place a Binance Futures MARKET order."
    )
    parser.add_argument("symbol", help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Order quantity, e.g., 0.01")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        qty = validate_positive_float(args.quantity, "quantity")

        order = place_market_order(symbol, side, qty)
        print("Market order placed. Order ID:", order.get("orderId"))

    except ValidationError as ve:
        msg = f"Validation error: {ve}"
        logger.error(msg)
        write_log_line(msg)
        print("Validation error:", ve)

    except Exception:
        print("Error placing market order. Check bot.log for details.")


if __name__ == "__main__":
    main()
