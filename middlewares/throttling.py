from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.cache = TTLCache(maxsize=10_000, ttl=1)

    async def __call__(self, handler, event: Message, data):
        if event.chat.id in self.cache:
            return
        self.cache[event.chat.id] = True
        return await handler(event, data)
