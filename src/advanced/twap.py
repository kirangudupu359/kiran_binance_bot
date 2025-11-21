# src/advanced/twap.py

import argparse
import time

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    ValidationError,
)

logger = get_logger("twap")


def run_twap(symbol: str, side: str, total_quantity: float,
            slices: int, interval_seconds: float):
    client = get_futures_client()
    slice_qty = round(total_quantity / slices, 8)  # prevent too many decimals

    logger.info(
        f"Starting TWAP: {side} {total_quantity} {symbol} "
        f"in {slices} slices every {interval_seconds} seconds "
        f"(slice size: {slice_qty})."
    )

    for i in range(1, slices + 1):
        logger.info(f"TWAP slice {i}/{slices}: {side} {slice_qty} {symbol}")
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=slice_qty,
            )
            logger.info(f"TWAP slice {i} placed: {order}")
        except Exception as exc:
            logger.exception(f"TWAP slice {i} failed: {exc}")

        if i < slices:
            time.sleep(interval_seconds)

    logger.info("TWAP complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Run a simple TWAP (Time-Weighted Average Price) strategy."
    )
    parser.add_argument("symbol")
    parser.add_argument("side")  # BUY or SELL
    parser.add_argument("total_quantity")
    parser.add_argument("slices", help="Number of slices, e.g., 5")
    parser.add_argument("interval_seconds", help="Seconds between slices, e.g., 10")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        total_qty = validate_positive_float(args.total_quantity, "total_quantity")
        slices = int(validate_positive_float(args.slices, "slices"))
        interval = validate_positive_float(args.interval_seconds, "interval_seconds")

        if slices < 1:
            raise ValidationError("slices must be >= 1")

        run_twap(symbol, side, total_qty, slices, interval)
        print("TWAP strategy finished. Check bot.log for slice details.")

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        print("Validation error:", ve)
    except Exception:
        print("Error running TWAP strategy. Check bot.log for details.")


if __name__ == "__main__":
    main()
