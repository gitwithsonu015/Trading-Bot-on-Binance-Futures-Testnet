from __future__ import annotations

import os
from typing import Any

import streamlit as st

from trading_bot.bot.client import BinanceConfig, BinanceUSDMClient
from trading_bot.bot.orders import place_order
from trading_bot.bot.validators import validate_order_input


st.set_page_config(page_title="Binance Futures Testnet Bot", layout="centered")

st.title("Binance Futures Testnet Bot")

st.caption("Creates MARKET/LIMIT orders on Binance USDT-M testnet.")

with st.sidebar:
    st.header("Credentials")
    api_key = os.getenv("BINANCE_TESTNET_API_KEY") or st.text_input("BINANCE_TESTNET_API_KEY", type="password")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET") or st.text_input(
        "BINANCE_TESTNET_API_SECRET", type="password"
    )

symbol = st.text_input("Symbol", value="BTCUSDT")
side = st.selectbox("Side", options=["BUY", "SELL"], index=0)
order_type = st.selectbox("Order type", options=["MARKET", "LIMIT"], index=0)
quantity = st.number_input("Quantity", min_value=0.0, value=0.001, step=0.001, format="%.10f")
price: float | None = None
if order_type == "LIMIT":
    price = st.number_input("Price", min_value=0.0, value=65000.0, step=1.0, format="%.10f")

is_dry_run = st.checkbox("Dry run (no API call)", value=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Place order"):
        try:
            validated = validate_order_input(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=float(quantity),
                price=float(price) if price is not None else None,
            )
        except Exception as e:
            st.error(f"Input validation failed: {e}")
            st.stop()

        st.subheader("Order request summary")
        st.json(
            {
                "symbol": validated.symbol,
                "side": validated.side,
                "type": validated.order_type,
                "quantity": validated.quantity,
                "price": validated.price,
                "dry_run": is_dry_run,
            }
        )

        if is_dry_run:
            st.info("Dry run enabled: no order was placed.")
            st.stop()

        if not api_key or not api_secret:
            st.error("Missing API credentials. Set env vars or fill in sidebar fields.")
            st.stop()

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
            st.success("SUCCESS")
            st.subheader("Order response")
            st.json(resp)
        except Exception as e:
            st.error(f"FAILURE: {e}")

