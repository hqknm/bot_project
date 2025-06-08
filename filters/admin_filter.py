from aiogram.filters import Filter
from aiogram.types import Message

class IsAdminFilter(Filter):
    key = "is_admin"

    async def __call__(self, message: Message) -> bool:
        from config.settings import ADMINS
        return message.from_user.id in ADMINS