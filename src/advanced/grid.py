# src/advanced/grid.py

import argparse
import numpy as np  # optional, but convenient

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    ValidationError,
)

logger = get_logger("grid")


def run_grid(symbol: str, side: str, total_quantity: float,
             lower_price: float, upper_price: float, levels: int):
    client = get_futures_client()

    logger.info(
        f"Starting GRID strategy for {symbol}: side={side}, "
        f"qty={total_quantity}, range=({lower_price}, {upper_price}), levels={levels}"
    )

    prices = np.linspace(lower_price, upper_price, levels)
    qty_per_level = round(total_quantity / levels, 8)

    for idx, price in enumerate(prices, start=1):
        logger.info(
            f"GRID level {idx}/{levels}: placing LIMIT {side} {qty_per_level} "
            f"{symbol} @ {price}"
        )
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=qty_per_level,
                price=str(price),
            )
            logger.info(f"GRID level {idx} order placed: {order}")
        except Exception as exc:
            logger.exception(f"GRID level {idx} failed: {exc}")

    logger.info("GRID setup finished.")


def main():
    parser = argparse.ArgumentParser(
        description="Run a simple grid strategy on Binance Futures."
    )
    parser.add_argument("symbol")
    parser.add_argument("side")  # BUY grid or SELL grid
    parser.add_argument("total_quantity")
    parser.add_argument("lower_price")
    parser.add_argument("upper_price")
    parser.add_argument("levels")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        total_qty = validate_positive_float(args.total_quantity, "total_quantity")
        lower = validate_positive_float(args.lower_price, "lower_price")
        upper = validate_positive_float(args.upper_price, "upper_price")
        levels = int(validate_positive_float(args.levels, "levels"))

        if levels < 2:
            raise ValidationError("levels must be >= 2")
        if lower >= upper:
            raise ValidationError("lower_price must be < upper_price")

        run_grid(symbol, side, total_qty, lower, upper, levels)
        print("Grid strategy initialized. Check bot.log for details.")

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        print("Validation error:", ve)
    except Exception:
        print("Error running grid strategy. Check bot.log for details.")


if __name__ == "__main__":
    main()
