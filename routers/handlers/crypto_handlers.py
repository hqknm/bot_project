from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.api_client import CoinGeckoAPI
from keyboards.builders import KeyboardBuilder
from keyboards.inline import main_menu
from utils.logger import setup_logger
from services.storage import Storage
from aiogram.exceptions import TelegramBadRequest
import time


logger = setup_logger(__name__)


router = Router(name="crypto_router")

api = CoinGeckoAPI()
storage = Storage()


@router.callback_query(F.data.startswith("fav_"))
async def toggle_favorite(callback: CallbackQuery):
    try:
        crypto_id = callback.data.split("_")[1]
        user_id = callback.from_user.id

        was_favorite = storage.is_favorite(user_id, crypto_id)

        if was_favorite:
            storage.remove_favorite(user_id, crypto_id)
            await callback.answer("❌ Удалено из избранного")
        else:
            storage.add_favorite(user_id, crypto_id)
            await callback.answer("⭐ Добавлено в избранное")
        storage.refresh_data()


        is_favorite = storage.is_favorite(user_id, crypto_id)
        crypto_data = await api.get_crypto_data(crypto_id)
        price = crypto_data['market_data']['current_price']['usd']
        change_24h = crypto_data['market_data']['price_change_percentage_24h']
        timestamp = int(time.time())
        message_text = (
            f"📊 <b>{crypto_data['name']} ({crypto_data['symbol'].upper()})</b>\n\n"
            f"💵 <b>Цена:</b> ${price:,.2f}\n"
            f"📈 <b>Изменение (24ч):</b> {change_24h:.2f}%\n"
            f"🏷️ <b>Капитализация:</b> ${crypto_data['market_data']['market_cap']['usd']:,}"
            f"\n\n🔄 Состояние: {'⭐ В избранном' if is_favorite else '❌ Не в избранном'}"
            f"\n⌚ {timestamp}"
        )

        keyboard = KeyboardBuilder().crypto_detail_buttons(
            crypto_id=crypto_id,
            is_favorite=is_favorite
        ).as_markup()

        try:
            # Пробуем обновить текст и клавиатуру
            await callback.message.edit_text(
                text=message_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except TelegramBadRequest:
            # Если не удалось изменить текст, обновляем только клавиатуру
            await callback.message.edit_reply_markup(reply_markup=keyboard)

    except Exception as e:
        logger.error(f"Error in toggle_favorite: {e}")
        await callback.answer("⚠️ Ошибка обновления", show_alert=True)


@router.callback_query(F.data == "top_crypto")
async def show_top_crypto(callback: CallbackQuery):
    try:
        if not api:
            await callback.answer("⚠️ Сервис временно недоступен", show_alert=True)
            return

        coins = await api.get_top_cryptos(limit=10)

        if not coins:
            await callback.answer("⚠️ Ошибка загрузки данных", show_alert=True)
            return

        message_text = "🏆 Топ-10 криптовалют:\n\n" + "\n".join(
            f"{idx + 1}. {coin['name']} ({coin['symbol'].upper()}) - ${coin['current_price']:,}"
            for idx, coin in enumerate(coins)
        )

        keyboard = KeyboardBuilder().top_coins_keyboard(coins).as_markup()
        await callback.message.edit_text(
            text=message_text,
            reply_markup=keyboard
        )
        logger.info(f"User {callback.from_user.id} requested top crypto")

    except Exception as e:
        logger.error(f"Error in show_top_crypto: {e}")
        await callback.answer("⚠️ Ошибка загрузки данных", show_alert=True)


@router.callback_query(F.data.startswith("crypto_"))
async def show_crypto_detail(callback: CallbackQuery):
    try:
        if not api:
            await callback.answer("⚠️ Сервис временно недоступен", show_alert=True)
            return

        crypto_id = callback.data.split("_")[1]
        is_favorite = storage.is_favorite(callback.from_user.id, crypto_id)

        crypto_data = await api.get_crypto_data(crypto_id)
        if not crypto_data:
            await callback.answer("❌ Данные не найдены", show_alert=True)
            return

        price = crypto_data['market_data']['current_price']['usd']
        change_24h = crypto_data['market_data']['price_change_percentage_24h']

        message_text = (
            f"📊 <b>{crypto_data['name']} ({crypto_data['symbol'].upper()})</b>\n\n"
            f"💵 <b>Цена:</b> ${price:,.2f}\n"
            f"📈 <b>Изменение (24ч):</b> {change_24h:.2f}%\n"
            f"🏷️ <b>Капитализация:</b> ${crypto_data['market_data']['market_cap']['usd']:,}"
        )

        keyboard = KeyboardBuilder().crypto_detail_buttons(
            crypto_id=crypto_id,
            is_favorite=is_favorite
        ).as_markup()

        await callback.message.edit_text(
            text=message_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info(f"User {callback.from_user.id} viewed {crypto_id}")

    except Exception as e:
        logger.error(f"Error in show_crypto_detail: {e}")
        await callback.answer("⚠️ Ошибка загрузки данных", show_alert=True)


@router.callback_query(F.data.startswith("chart_"))
async def show_crypto_chart(callback: CallbackQuery):
    try:
        if not api:
            await callback.answer("⚠️ Сервис временно недоступен", show_alert=True)
            return

        _, crypto_id, period = callback.data.split("_")
        chart_data = await api.get_crypto_chart(crypto_id, period)

        if not chart_data:
            await callback.answer("❌ Ошибка загрузки графика", show_alert=True)
            return

        # Здесь должна быть логика генерации/отправки графика
        # Временная заглушка:
        await callback.message.answer(
            f"📊 График для {crypto_id.upper()} за {period} дней\n"
            f"(реальная реализация требует интеграции с графической библиотекой)"
        )
        logger.info(f"User {callback.from_user.id} viewed chart for {crypto_id}")

    except Exception as e:
        logger.error(f"Error in show_crypto_chart: {e}")
        await callback.answer("⚠️ Ошибка генерации графика", show_alert=True)


@router.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🏠 Главное меню",
        reply_markup=main_menu()
    )
__all__ = ['router']