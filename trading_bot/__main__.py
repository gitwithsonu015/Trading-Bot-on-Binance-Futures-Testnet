from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BINANCE_TESTNET_API_KEY")
api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

from trading_bot.bot.cli import main

if __name__ == "__main__":
    main()


