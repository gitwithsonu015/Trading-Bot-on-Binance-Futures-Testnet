from __future__ import annotations

import re
from dataclasses import dataclass


_SYMBOL_RE = re.compile(r"^[A-Z0-9]{1,20}$")


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


@dataclass(frozen=True)
class OrderInput:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not _SYMBOL_RE.match(s):
        raise ValueError("symbol must be uppercase alphanumerics like BTCUSDT (e.g., BTCUSDT)")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValueError("side must be BUY or SELL")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValueError("order type must be MARKET or LIMIT")
    return t


def validate_quantity(quantity: float) -> float:
    try:
        q = float(quantity)
    except Exception as e:
        raise ValueError("quantity must be a number") from e
    if q <= 0:
        raise ValueError("quantity must be > 0")
    return q


def validate_price(price: float | None, order_type: str) -> float | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("price is required for LIMIT orders")
        try:
            p = float(price)
        except Exception as e:
            raise ValueError("price must be a number") from e
        if p <= 0:
            raise ValueError("price must be > 0")
        return p

    # MARKET
    if price is not None:
        raise ValueError("price must be omitted for MARKET orders")
    return None


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> OrderInput:
    symbol_v = validate_symbol(symbol)
    side_v = validate_side(side)
    type_v = validate_order_type(order_type)
    qty_v = validate_quantity(quantity)
    price_v = validate_price(price, type_v)
    return OrderInput(symbol=symbol_v, side=side_v, order_type=type_v, quantity=qty_v, price=price_v)

