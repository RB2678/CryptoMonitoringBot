import os
from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

COIN_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "ton": "the-open-network",
    "doge": "dogecoin"
}

REVERSE_MAP = {v: k for k, v in COIN_MAP.items()}
