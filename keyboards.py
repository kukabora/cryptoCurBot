from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Начать!', callback_data='start')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_2 = InlineKeyboardButton('Личный кабинет', callback_data='cabinet')
inline_btn_3 = InlineKeyboardButton('Обменник', callback_data='tradeBtn')
inline_btn_4 = InlineKeyboardButton('Магазин', callback_data='store')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2, inline_btn_3, inline_btn_4)

inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
inline_btn_8 = InlineKeyboardButton('Назад', callback_data='backToMenu')
cabinetKB = InlineKeyboardMarkup().add(inline_btn_5, inline_btn_6, inline_btn_7, inline_btn_8)

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

inline_btn_19 = InlineKeyboardButton('Бабанокоин', callback_data='babanoTrade1')
inline_btn_20 = InlineKeyboardButton('Мнепохуйтокен', callback_data='mnepohuiTrade1')
inline_btn_21 = InlineKeyboardButton('Гослингкоин', callback_data='goslingTrade1')
inline_btn_22 = InlineKeyboardButton('Рэддублон', callback_data='redTrade1')
inline_btn_23 = InlineKeyboardButton('Попакоин', callback_data='popaTrade1')
inline_btn_24 = InlineKeyboardButton('Душнилатокин', callback_data='dushnilaTrade1')
inline_btn_25 = InlineKeyboardButton('паааакоин)', callback_data='paaaTrade1')
inline_btn_26 = InlineKeyboardButton('Туринариум', callback_data='turinaTrade1')
inline_btn_27 = InlineKeyboardButton('Чак-Чак', callback_data='chakTrade1')
inline_btn_28 = InlineKeyboardButton('Дохлаямонета', callback_data='dohlayaTrade1')
trade1KB = InlineKeyboardMarkup().add(inline_btn_19, inline_btn_20, inline_btn_21, inline_btn_22, inline_btn_23, inline_btn_24, inline_btn_25, inline_btn_26, inline_btn_27, inline_btn_28)
trade1KB.row(inline_btn_8)


