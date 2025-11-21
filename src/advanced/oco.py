# src/advanced/oco.py

import argparse
import uuid

from client import get_futures_client
from utils import (
    get_logger,
    validate_symbol,
    validate_side,
    validate_positive_float,
    ValidationError,
)

logger = get_logger("oco")


def place_oco_orders(symbol: str, side: str, quantity: float,
                     take_profit_price: float,
                     stop_price: float,
                     stop_limit_price: float):
    """
    Simple OCO-like behaviour for futures:
    - One LIMIT order at take_profit_price
    - One STOP-LIMIT order at stop_limit_price with stop_price trigger
    """
    client = get_futures_client()

    oco_group_id = str(uuid.uuid4())
    logger.info(
        f"Placing OCO group {oco_group_id} for {symbol} {side} {quantity}: "
        f"TP={take_profit_price}, SL stop={stop_price}, SL limit={stop_limit_price}"
    )

    try:
        # Take-profit limit order
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(take_profit_price),
            stopPrice=str(take_profit_price),
            reduceOnly=True,
            workingType="MARK_PRICE",
            newClientOrderId=f"tp_{oco_group_id}",
        )

        # Stop-limit order as stop-loss
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=str(stop_limit_price),
            stopPrice=str(stop_price),
            reduceOnly=True,
            workingType="MARK_PRICE",
            newClientOrderId=f"sl_{oco_group_id}",
        )

        logger.info(
            f"OCO group {oco_group_id} placed. "
            f"TP order: {tp_order}, SL order: {sl_order}"
        )

        return {"oco_group_id": oco_group_id,
                "take_profit_order": tp_order,
                "stop_loss_order": sl_order}

    except Exception as exc:
        logger.exception(f"Failed to place OCO group {oco_group_id}: {exc}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Place a simulated OCO (take-profit + stop-loss) on Binance Futures."
    )
    parser.add_argument("symbol")
    parser.add_argument("side")  # BUY or SELL position to close
    parser.add_argument("quantity")
    parser.add_argument("take_profit_price")
    parser.add_argument("stop_price")
    parser.add_argument("stop_limit_price")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        qty = validate_positive_float(args.quantity, "quantity")
        tp = validate_positive_float(args.take_profit_price, "take_profit_price")
        stop = validate_positive_float(args.stop_price, "stop_price")
        stop_limit = validate_positive_float(args.stop_limit_price, "stop_limit_price")

        result = place_oco_orders(symbol, side, qty, tp, stop, stop_limit)
        print("OCO group placed. Group ID:", result["oco_group_id"])

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        print("Validation error:", ve)
    except Exception:
        print("Error placing OCO orders. Check bot.log for details.")


if __name__ == "__main__":
    main()
