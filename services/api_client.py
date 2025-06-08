import aiohttp
import cachetools
from config.settings import COINGECKO_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CoinGeckoAPI:
    def __init__(self):
        self.cache = cachetools.TTLCache(maxsize=100, ttl=60)
        self.timeout = aiohttp.ClientTimeout(total=10)
        self.session = None

    async def init_session(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)

    async def close_session(self):
        if self.session:
            await self.session.close()

    async def _get(self, endpoint, params=None):
        """Общий метод для GET-запросов"""
        try:
            if not self.session:
                await self.init_session()

            url = f"{COINGECKO_URL}{endpoint}"
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"API request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    async def get_top_cryptos(self, limit=10):
        cache_key = f"top_{limit}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h"
        }

        data = await self._get("/coins/markets", params)
        if data:
            self.cache[cache_key] = data
        return data

    async def get_crypto_data(self, crypto_id: str):
        cache_key = f"crypto_{crypto_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        }

        data = await self._get(f"/coins/{crypto_id}", params)
        if data:
            self.cache[cache_key] = data
        return data

    async def get_crypto_chart(self, crypto_id: str, days: str):
        try:
            days_value = int(days.replace('d', ''))
        except ValueError:
            days_value = 7

        cache_key = f"chart_{crypto_id}_{days_value}d"
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {
            "vs_currency": "usd",
            "days": days_value,
            "interval": "daily"
        }

        data = await self._get(f"/coins/{crypto_id}/market_chart", params)
        if data:
            self.cache[cache_key] = data
        return data