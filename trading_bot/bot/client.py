from __future__ import annotations

import hashlib
import hmac
import logging
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)


TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceAPIError(RuntimeError):
    pass


@dataclass(frozen=True)
class BinanceConfig:
    api_key: str
    api_secret: str
    base_url: str = TESTNET_BASE_URL
    recv_window_ms: int = 5000
    # Futures testnet uses the same security model as live.


class BinanceUSDMClient:
    def __init__(self, config: BinanceConfig, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session or requests.Session()

    def _sign(self, query_string: str) -> str:
        secret = self.config.api_secret.encode("utf-8")
        message = query_string.encode("utf-8")
        return hmac.new(secret, message, hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self.config.base_url + path
        params = dict(params or {})
        params.setdefault("recvWindow", self.config.recv_window_ms)
        params.setdefault("timestamp", int(time.time() * 1000))

        # Sign full query string
        # NOTE: binance expects the signature over the querystring without leading '?'
        query_string = urlencode(params, doseq=True)
        signature = self._sign(query_string)
        signed_query = f"{query_string}&signature={signature}"

        headers = {"X-MBX-APIKEY": self.config.api_key}

        # Log request (avoid leaking secret)
        logger.info("Binance request %s %s params=%s", method, path, {k: params[k] for k in params if k != "signature"})
        logger.debug("Signed query=%s", signed_query)

        try:
            resp = self.session.request(method=method, url=url, headers=headers, data=signed_query, timeout=30)
        except requests.RequestException as e:
            logger.exception("Network error calling Binance")
            raise

        logger.info("Binance response status=%s", resp.status_code)
        logger.debug("Binance response body=%s", resp.text)

        if not resp.ok:
            raise BinanceAPIError(f"Binance API error: HTTP {resp.status_code}: {resp.text}")

        try:
            data = resp.json()
        except Exception as e:
            raise BinanceAPIError(f"Non-JSON response: {resp.text}") from e

        if isinstance(data, dict) and "code" in data and "msg" in data:
            raise BinanceAPIError(f"Binance API error: {data.get('code')} {data.get('msg')}")

        return data

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> dict[str, Any]:
        path = "/fapi/v1/order"
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT")
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._request("POST", path, params=params)

