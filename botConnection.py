import logging
from dataBase import DB
import keyboards as kb
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types

db = DB()

API_TOKEN = db.getBotToken()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

###Кнопки
@dp.callback_query_handler(lambda c: c.data == 'start' or c.data == "backToMenu") 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} started the bot.")
    if (not len(db.findUserById(callback_query.from_user.id))):
        db.createNewUser(str(callback_query.from_user.id), str(callback_query.from_user.username))
        db.createNewWallet(str(callback_query.from_user.id))
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="С чего начнём?", reply_markup=kb.inline_kb2)

@dp.callback_query_handler(lambda c: c.data == 'cabinet')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered cabinet.")
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Добро пожаловать в ваш личный кабинет", reply_markup=cabinetKB)

@dp.callback_query_handler(lambda c: c.data == 'store')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered store.")
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Нинада ломать бота я вижу тебя, {callback_query.from_user.username}", reply_markup=kb.testKB)

@dp.callback_query_handler(lambda c: c.data == 'tradeBtn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered exchange section.")
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Нинада ломать бота я вижу тебя, {callback_query.from_user.username}", reply_markup=kb.testKB)

@dp.callback_query_handler(lambda c: c.data == 'balance')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is checking his balance.")
    await bot.answer_callback_query(callback_query.id)
    balance = db.getWalletBuyUserId(callback_query.from_user.id)
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=
    f"""
    *Ваш баланс составляет:*


    🐥Бабанокоин: ({balance[2]})
    Мнепохуйтокен: ({balance[3]})
    💰Гослингкоин: ({balance[4]})
    Попакоин: ({balance[5]})
    👾Душнилатокин: ({balance[6]})
    🕷паааакоин): ({balance[7]})
    💊Туринариум: ({balance[8]})
    Чак-Чак: ({balance[9]})
    🦽ДохлаяМонета: ({balance[10]})

    В общей сложности это составляет 0 Кекекоинов.
    """, parse_mode="Markdown", reply_markup=cabinetKB)

###Команды
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.answer(
        """

    Привет!
    Я персональный кекестанский помощник по крипте!
    С моей помощью вы можете легко обменивать свои (и не только свои) токены
    а так же покупать за них различные услуги.
    
    Начнем?
    """,
    reply_markup=kb.inline_kb1
    )

###Всё остальное
@dp.message_handler()
async def nonExistingCommand(message: types.Message):
    if (message.text[0] == "/"):
        await message.answer("Нет такой команды. \nМне похуй.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)