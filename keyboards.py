from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Начать!', callback_data='start')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_2 = InlineKeyboardButton('Личный кабинет', callback_data='cabinet')
inline_btn_3 = InlineKeyboardButton('Обменник', callback_data='tradeBtn')
inline_btn_4 = InlineKeyboardButton('Магазин', callback_data='store')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2, inline_btn_3, inline_btn_4)

inline_btn_8 = InlineKeyboardButton('Назад', callback_data='backToMenu')

testBtn = InlineKeyboardButton('штош)', callback_data='start')
testKB = InlineKeyboardMarkup().add(testBtn)


addGoodBtn = InlineKeyboardButton('Добавить товар', callback_data='addGood')
delGoodBtn = InlineKeyboardButton('Удалить товар', callback_data='delGood')
previewBtn = InlineKeyboardButton('Предпросмотр', callback_data='storePreview')
backToCabinetBtn = InlineKeyboardButton('Назад', callback_data='cabinet')

storeSettings = InlineKeyboardMarkup().row(addGoodBtn, delGoodBtn, previewBtn)
storeSettings.row(backToCabinetBtn)

cancelButton = KeyboardButton("◀️Назад")