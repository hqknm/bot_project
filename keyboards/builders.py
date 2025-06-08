from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List


class KeyboardBuilder:
    @staticmethod
    def crypto_detail_buttons(crypto_id: str, is_favorite: bool) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        builder.button(text="📈 7 дней", callback_data=f"chart_{crypto_id}_7d")
        builder.button(text="📉 30 дней", callback_data=f"chart_{crypto_id}_30d")

        favorite_text = "❌ Удалить" if is_favorite else "⭐ В избранное"
        builder.button(text=favorite_text, callback_data=f"fav_{crypto_id}")
        builder.button(text="🔙 Назад", callback_data="top_crypto")

        builder.adjust(2, 1, 1)
        return builder

    @staticmethod
    def favorites_keyboard(favorites: List[str]) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for crypto_id in favorites:
            builder.button(text=crypto_id.upper(), callback_data=f"crypto_{crypto_id}")
        builder.button(text="🔙 Главное меню", callback_data="main_menu")
        builder.adjust(1)
        return builder

    @staticmethod
    def top_coins_keyboard(coins: list) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for coin in coins:
            builder.button(
                text=coin['symbol'].upper(),
                callback_data=f"crypto_{coin['id']}"
            )
        builder.button(text="🔙 Главное меню", callback_data="main_menu")
        builder.adjust(3, 3, 3, 1)
        return builder

    @staticmethod
    def confirmation_keyboard() -> InlineKeyboardBuilder:
        """Клавиатура для подтверждения действий"""
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Да", callback_data="confirm_yes")
        builder.button(text="❌ Нет", callback_data="confirm_no")
        return builder

    @staticmethod
    def favorites_keyboard(favorites: List[str]) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for crypto_id in favorites:
            builder.button(text=crypto_id.upper(), callback_data=f"crypto_{crypto_id}")

        # Добавляем кнопку обновления
        builder.button(text="🔄 Обновить", callback_data="refresh_favorites")
        builder.button(text="🔙 Главное меню", callback_data="main_menu")
        builder.adjust(1, 2)  # Обновляем раскладку
        return builder