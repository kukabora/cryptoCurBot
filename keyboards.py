from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_1 = InlineKeyboardButton('Начать!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
