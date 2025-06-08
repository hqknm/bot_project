import asyncio
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN
from utils.logger import setup_logger
from routers import commands, admin
from routers.handlers import crypto_handlers, favorites_handlers
from services.storage import Storage
from services.api_client import CoinGeckoAPI

logger = setup_logger()


async def main():
    api_client = CoinGeckoAPI()
    storage = Storage()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp["api_client"] = api_client
    dp["storage"] = storage

    dp.include_router(commands.router)
    dp.include_router(crypto_handlers.router)
    dp.include_router(favorites_handlers.router)
    dp.include_router(admin.router)

    # 4. Запуск
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())