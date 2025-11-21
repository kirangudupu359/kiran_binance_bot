# src/utils.py

import logging
import re

LOG_FILE = "bot.log"

class ValidationError(Exception):
    """Raised when user input is invalid."""
    pass


# ------------ LOGGING SETUP ------------
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)

# Prevent adding duplicate handlers
if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    return logger


# ------------ VALIDATION HELPERS ------------

def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    if not re.fullmatch(r"[A-Z]+USDT", symbol):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Use USDT-margined pairs like BTCUSDT, ETHUSDT."
        )
    return symbol


def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValidationError("Side must be BUY or SELL.")
    return side


def validate_positive_float(raw: str, field_name: str) -> float:
    try:
        value = float(raw)
    except ValueError:
        raise ValidationError(f"{field_name} must be a number.")
    if value <= 0:
        raise ValidationError(f"{field_name} must be > 0.")
    return value


def validate_price_hierarchy(stop_price: float, limit_price: float, side: str):
    if side == "BUY" and stop_price > limit_price:
        raise ValidationError(
            "For BUY stop-limit: stop_price should be <= limit_price."
        )
    if side == "SELL" and stop_price < limit_price:
        raise ValidationError(
            "For SELL stop-limit: stop_price should be >= limit_price."
        )
