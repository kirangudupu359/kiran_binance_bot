# src/limit_orders.py

import argparse

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    ValidationError,
)

logger = get_logger("limit_orders")


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    client = get_futures_client()
    logger.info(f"Sending LIMIT order: {side} {quantity} {symbol} @ {price}")

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price),  # Binance expects string for price in some cases
        )
        logger.info(f"LIMIT order placed successfully: {order}")
        return order
    except Exception as exc:
        logger.exception(f"Failed to place LIMIT order: {exc}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Place a Binance Futures LIMIT order."
    )
    parser.add_argument("symbol", help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Order quantity, e.g., 0.01")
    parser.add_argument("price", help="Limit price, e.g., 65000")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        qty = validate_positive_float(args.quantity, "quantity")
        price = validate_positive_float(args.price, "price")

        order = place_limit_order(symbol, side, qty, price)
        print("Limit order placed. Order ID:", order.get("orderId"))

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        print("Validation error:", ve)
    except Exception:
        print("Error placing limit order. Check bot.log for details.")


if __name__ == "__main__":
    main()
