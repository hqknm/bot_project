from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Топ криптовалют", callback_data="top_crypto")
    builder.button(text="⭐ Избранное", callback_data="favorites")
    builder.adjust(1)
    return builder.as_markup()

def back_to_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Главное меню", callback_data="main_menu")
    return builder.as_markup()