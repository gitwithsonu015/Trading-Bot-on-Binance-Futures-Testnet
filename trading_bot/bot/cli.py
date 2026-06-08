from __future__ import annotations

import argparse
import logging
import os
from typing import Any

from trading_bot.bot.client import BinanceConfig, BinanceUSDMClient, BinanceAPIError
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import place_order
from trading_bot.bot.validators import validate_order_input

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Simplified Binance USDT-M Futures Testnet trading bot")
    p.add_argument("--symbol", required=True, help="e.g., BTCUSDT")
    p.add_argument("--side", required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    p.add_argument("--type", required=True, dest="order_type", choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    p.add_argument("--quantity", required=True, type=float, help="Order quantity")
    p.add_argument("--price", type=float, default=None, help="Required for LIMIT orders")

    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Build/validate the request but do not place order (no API call).",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

    try:
        validated = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as e:
        print(f"Input error: {e}")
        raise SystemExit(2)

    print("Order request summary")
    print(f"  symbol={validated.symbol}")
    print(f"  side={validated.side}")
    print(f"  type={validated.order_type}")
    print(f"  quantity={validated.quantity}")
    if validated.price is not None:
        print(f"  price={validated.price}")

    if args.dry_run:
        print("Dry-run enabled: no order was placed.")
        return

    if not api_key or not api_secret:
        print("Missing credentials. Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET environment variables.")
        raise SystemExit(3)

    client = BinanceUSDMClient(BinanceConfig(api_key=api_key, api_secret=api_secret))

    try:
        resp = place_order(
            client,
            symbol=validated.symbol,
            side=validated.side,
            order_type=validated.order_type,
            quantity=validated.quantity,
            price=validated.price,
        )

        print("Order response")
        print(f"  orderId={resp.get('orderId')}")
        print(f"  status={resp.get('status')}")
        print(f"  executedQty={resp.get('executedQty')}")
        print(f"  avgPrice={resp.get('avgPrice')}")
        print("SUCCESS")

    except BinanceAPIError as e:
        logger.exception("Binance API error")
        print(f"FAILURE: {e}")
        raise SystemExit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"FAILURE: {e}")
        raise SystemExit(1)

