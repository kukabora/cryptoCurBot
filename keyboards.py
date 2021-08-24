from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Начать!', callback_data='start')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_2 = InlineKeyboardButton('Личный кабинет', callback_data='cabinet')
inline_btn_3 = InlineKeyboardButton('Обменник', callback_data='tradeBtn')
inline_btn_4 = InlineKeyboardButton('Магазин', callback_data='store')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2, inline_btn_3, inline_btn_4)

inline_btn_8 = InlineKeyboardButton('Назад', callback_data='backToMenu')

inline_btn_9 = InlineKeyboardButton('Бабанокоин', callback_data='babanobuy')
inline_btn_10 = InlineKeyboardButton('Мнепохуйтокен', callback_data='mnepohuibuy')
inline_btn_11 = InlineKeyboardButton('Гослингкоин', callback_data='goslingbuy')
inline_btn_12 = InlineKeyboardButton('Рэддублон', callback_data='redbuy')
inline_btn_13 = InlineKeyboardButton('Попакоин', callback_data='popabuy')
inline_btn_14 = InlineKeyboardButton('Душнилатокин', callback_data='dushnilabuy')
inline_btn_15 = InlineKeyboardButton('паааакоин)', callback_data='paaabuy')
inline_btn_16 = InlineKeyboardButton('Туринариум', callback_data='turinabuy')
inline_btn_17 = InlineKeyboardButton('Чак-Чак', callback_data='chakbuy')
inline_btn_18 = InlineKeyboardButton('Дохлаямонета', callback_data='dohlayabuy')
buyKB = InlineKeyboardMarkup().add(inline_btn_9, inline_btn_10, inline_btn_11, inline_btn_12, inline_btn_13, inline_btn_14, inline_btn_15, inline_btn_16, inline_btn_17, inline_btn_18)
buyKB.row(inline_btn_8)





testBtn = InlineKeyboardButton('штош)', callback_data='start')
testKB = InlineKeyboardMarkup().add(testBtn)
