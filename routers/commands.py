from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu
from filters.command_filter import IsCommand
from aiogram.filters import Command
from services.api_client import CoinGeckoAPI
from services.storage import Storage
from keyboards.builders import KeyboardBuilder
import time
router = Router()
api = CoinGeckoAPI()
storage = Storage()

@router.message(IsCommand())
async def unknown_command(message: Message):
    await message.answer(
        "⚠️ Неизвестная команда. Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Справка\n"
        "/list - Топ криптовалют\n"
        "/favorites - Избранное"
    )

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "🚀 Добро пожаловать в Crypto Tracker Bot!\n"
        "Отслеживайте курсы криптовалют в реальном времени",
        reply_markup=main_menu()
    )

@router.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer(
        "📚 Доступные команды:\n"
        "/list - Топ-10 криптовалют\n"
        "/price [код] - Цена монеты (например: /price bitcoin)\n"
        "/favorites - Ваши избранные монеты\n"
        "/chart [код] - График за 7 дней"
    )

@router.message(Command("list"))
async def cmd_list(message: Message):
    coins = await api.get_top_cryptos(limit=10)
    message_text = "🏆 Топ-10 криптовалют:\n\n" + "\n".join(
        f"{idx + 1}. {coin['name']} ({coin['symbol'].upper()}) - ${coin['current_price']:,}"
        for idx, coin in enumerate(coins)
    )
    keyboard = KeyboardBuilder().top_coins_keyboard(coins).as_markup()
    await message.answer(message_text, reply_markup=keyboard)


@router.message(Command("price"))
async def cmd_price(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("ℹ️ Использование: /price <код_валюты>")

    crypto_id = args[1].lower()
    crypto_data = await api.get_crypto_data(crypto_id)
    price = crypto_data['market_data']['current_price']['usd']
    await message.answer(f"💵 {crypto_data['name']}: ${price:,.2f}")


@router.message(Command("favorites"))
async def cmd_favorites(message: Message):
    favorites = storage.get_favorites(message.from_user.id)
    if not favorites:
        return await message.answer("⭐ Избранное пусто")

    timestamp = int(time.time())
    text = f"⭐ Ваши избранные монеты (обновлено: {timestamp}):"

    keyboard = KeyboardBuilder().favorites_keyboard(favorites).as_markup()

    await message.answer(
        text,
        reply_markup=keyboard
    )


@router.message(Command("chart"))
async def cmd_chart(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("ℹ️ Использование: /chart <код_валюты>")

    crypto_id = args[1].lower()
    await message.answer(f"📊 График для {crypto_id} (реализация в разработке)")
@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🏠 Вы вернулись в главное меню",
        reply_markup=main_menu()
    )