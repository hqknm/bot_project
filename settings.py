import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [int(id) for id in os.getenv("ADMINS").split(",")] if os.getenv("ADMINS") else []
COINGECKO_URL = "https://api.coingecko.com/api/v3"