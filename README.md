# Trading Bot (Binance Futures USDT-M Testnet)

A simplified Python trading bot that can place **MARKET** and **LIMIT** orders on Binance **USDT-M Futures Testnet**.

## Features
- CLI input via `argparse`
- BUY / SELL support
- MARKET / LIMIT support
- Structured code:
  - `trading_bot/bot/client.py`: REST client (signed requests + logging)
  - `trading_bot/bot/orders.py`: order placement logic
  - `trading_bot/bot/validators.py`: input validation
  - `trading_bot/bot/cli.py`: CLI entry point
- Logging to `trading_bot.log` (requests/responses/errors)

## Prerequisites
- Python 3.x
- Binance Futures Testnet account
- API credentials with trading enabled

## Setup
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (required for real order placement):
   - `BINANCE_TESTNET_API_KEY`
   - `BINANCE_TESTNET_API_SECRET`

## Run Examples
### Dry run (no API call)
```bash
python -m trading_bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
python -m trading_bot --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000 --dry-run
```

### Place a MARKET order
```bash
python -m trading_bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order
```bash
python -m trading_bot --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

## Optional: Lightweight UI (Streamlit)
Run:
```bash
streamlit run trading_bot/ui.py
```

The UI reuses the same validators + order placement logic. Use **Dry run** first.

## Output
The app prints:
- order request summary
- order response details (`orderId`, `status`, `executedQty`, `avgPrice` if available)
- `SUCCESS` or `FAILURE`


## Logging
- Logs are written to: `trading_bot.log`
- Includes request/response status and errors (API secrets are not logged)

## Assumptions
- This bot does **not** manage leverage/margin settings.
- You must ensure the symbol exists on the testnet and your account has sufficient margin.

## Note
Base URL used for all API interactions:
- https://testnet.binancefuture.com
