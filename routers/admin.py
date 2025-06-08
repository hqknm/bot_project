from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.admin_filter import IsAdminFilter
from services.storage import Storage
from config.settings import ADMINS
router = Router()
router.message.filter(IsAdminFilter())

class BroadcastState(StatesGroup):
    waiting_message = State()

@router.message(F.text == "/stats")
async def cmd_stats(message: Message, storage: Storage):
    users_count = len(storage.data)
    await message.answer(f"👥 Пользователей: {users_count}")

@router.message(F.text == "/broadcast")
async def start_broadcast(message: Message, state: FSMContext):
    await message.answer("Введите сообщение для рассылки:")
    await state.set_state(BroadcastState.waiting_message)

@router.message(BroadcastState.waiting_message)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot, storage: Storage):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ У вас нет прав на рассылку")
        await state.clear()
        return
    for user_id in storage.data.keys():
        try:
            await bot.send_message(user_id, message.text)
        except Exception as e:
            print(f"Ошибка отправки {user_id}: {e}")
    await state.clear()


@router.message(F.text.startswith("/ban "))
async def cmd_ban(message: Message, storage: Storage):
    user_id = int(message.text.split()[1])
    storage.ban_user(user_id)
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("❌ Неверный формат: /ban <user_id>")
    await message.answer(f"Пользователь {user_id} заблокирован")