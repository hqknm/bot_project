from aiogram import BaseMiddleware
from services.storage import Storage


class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        storage: Storage = data["storage"]
        user_id = event.from_user.id

        if storage.is_banned(user_id):
            await event.answer("❌ Вы заблокированы")
            return
        return await handler(event, data)