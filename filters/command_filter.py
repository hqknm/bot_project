from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsCommand(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.text or not message.text.startswith('/'):
            return False

        command = message.text.split()[0][1:].lower()

        known_commands = {'start', 'help', 'stats', 'broadcast', 'ban',
                          'list', 'price', 'favorites', 'chart'}  # Удалено 'settings'
        return command not in known_commands