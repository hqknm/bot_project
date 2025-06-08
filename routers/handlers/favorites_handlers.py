from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.builders import KeyboardBuilder
from keyboards.inline import back_to_main_menu
from services.storage import Storage
from aiogram.exceptions import TelegramBadRequest
import time

router = Router()
storage = Storage()

@router.callback_query(F.data == "favorites")
async def show_favorites(callback: CallbackQuery):
    storage.refresh_data()
    user_id = callback.from_user.id
    favorites = storage.get_favorites(user_id)

    if not favorites:
        await callback.message.edit_text(
            text="⭐ У вас пока нет избранных монет.\nДобавьте их через детальный просмотр монеты.",
            reply_markup=back_to_main_menu()
        )
        return

    timestamp = int(time.time())
    text = f"⭐ Ваши избранные монеты (обновлено: {timestamp}):"

    keyboard = KeyboardBuilder().favorites_keyboard(favorites).as_markup()

    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        await callback.message.edit_reply_markup(reply_markup=keyboard)

@router.callback_query(F.data == "refresh_favorites")
async def refresh_favorites(callback: CallbackQuery):
    storage.refresh_data()
    user_id = callback.from_user.id
    favorites = storage.get_favorites(user_id)

    if not favorites:
        await callback.answer("⭐ У вас пока нет избранных монет")
        return

    timestamp = int(time.time())
    text = f"⭐ Ваши избранные монеты (обновлено: {timestamp}):"

    keyboard = KeyboardBuilder().favorites_keyboard(favorites).as_markup()

    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        try:
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        except TelegramBadRequest:
            await callback.answer("✅ Список актуален")
            return

    await callback.answer("✅ Список обновлен")