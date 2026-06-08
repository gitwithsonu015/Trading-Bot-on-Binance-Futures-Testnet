from __future__ import annotations

import logging
from typing import Any

from trading_bot.bot.client import BinanceUSDMClient

logger = logging.getLogger(__name__)


def normalize_order_response(resp: dict[str, Any]) -> dict[str, Any]:
    return {
        "orderId": resp.get("orderId"),
        "status": resp.get("status"),
        "executedQty": resp.get("executedQty"),
        "avgPrice": resp.get("avgPrice"),
        "symbol": resp.get("symbol"),
        "side": resp.get("side"),
        "type": resp.get("type"),
    }


def place_order(client: BinanceUSDMClient, *, symbol: str, side: str, order_type: str, quantity: float, price: float | None = None) -> dict[str, Any]:
    logger.info("Placing order %s %s %s qty=%s price=%s", symbol, side, order_type, quantity, price)
    resp = client.create_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price)
    return normalize_order_response(resp)

