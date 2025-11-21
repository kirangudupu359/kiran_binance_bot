# src/advanced/stop_limit.py

import argparse

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    validate_price_hierarchy,
    ValidationError,
)

logger = get_logger("stop_limit")


def place_stop_limit_order(symbol: str, side: str, quantity: float,
                           stop_price: float, limit_price: float):
    client = get_futures_client()
    logger.info(
        f"Sending STOP-LIMIT order: {side} {quantity} {symbol}, "
        f"stop={stop_price}, limit={limit_price}"
    )

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",              # STOP = stop-limit in futures
            timeInForce="GTC",
            quantity=quantity,
            price=str(limit_price),
            stopPrice=str(stop_price),
            workingType="MARK_PRICE",  # trigger based on mark price
        )
        logger.info(f"STOP-LIMIT order placed: {order}")
        return order
    except Exception as exc:
        logger.exception(f"Failed to place STOP-LIMIT order: {exc}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Place a Binance Futures STOP-LIMIT order."
    )
    parser.add_argument("symbol")
    parser.add_argument("side")          # BUY or SELL
    parser.add_argument("quantity")
    parser.add_argument("stop_price")
    parser.add_argument("limit_price")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        qty = validate_positive_float(args.quantity, "quantity")
        stop_price = validate_positive_float(args.stop_price, "stop_price")
        limit_price = validate_positive_float(args.limit_price, "limit_price")
        validate_price_hierarchy(stop_price, limit_price, side)

        order = place_stop_limit_order(symbol, side, qty, stop_price, limit_price)
        print("Stop-limit order placed. Order ID:", order.get("orderId"))

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        print("Validation error:", ve)
    except Exception:
        print("Error placing stop-limit order. Check bot.log for details.")


if __name__ == "__main__":
    main()
