import logging
from dataBase import DB
import keyboards as kb
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
import re
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from states import States

db = DB()

API_TOKEN = db.getBotToken()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

TestStates = States()
###Хэндлеры состояний
@dp.message_handler(state=TestStates.all()[3])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text.isdigit():
        if message.text in db.getAllStoreGoodsByID(message.from_user.id):
            await state.reset_state()
            db.deleteGood(message.text)
            await message.answer(f"Товар успешно удалён!", reply_markup=kb.storeSettings)
        else:
            await message.answer(f"Хитрожопый дохуя? У тебя нет товара с таким айди")

    else:
        await message.answer(f"Цифрами блять напиши цену, что непонятного?", reply=False)

@dp.message_handler(state=TestStates.all()[2])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    db.updateGoodInfo(message.from_user.id, "description", f"'{message.text}'")
    await state.reset_state()
    await message.answer(f"Товар успешно добавлен!",  reply_markup=kb.storeSettings)

@dp.message_handler(state=TestStates.all()[1])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text.isdigit():
        db.updateGoodInfo(message.from_user.id, "price", f"{message.text}")
        await state.set_state(TestStates.all()[2])
        tokenInfo = db.getTokenInfoByOwnerId(message.from_user.id)
        await message.answer(f"В двух словах опишите ваш товар (максимум - 400 символов): ", reply=False)
    else:
        await message.answer(f"Цифрами блять напиши цену, что непонятного?", reply=False)

@dp.message_handler(state=TestStates.all()[0])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    db.updateGoodInfo(message.from_user.id, "name", f"'{message.text}'")
    await state.set_state(TestStates.all()[1])
    tokenInfo = db.getTokenInfoByOwnerId(message.from_user.id)
    await message.answer(f"Отправьте, пожалуйста, цену товара в своей валюте ({tokenInfo[1]}):", reply_markup=None)

###Кнопки

@dp.callback_query_handler(lambda c: c.data == 'delGood') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is deleting single good in his store.")
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(TestStates.all()[3])
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f"""Введите айди товара, который хотите удалить: """, parse_mode="html", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == 'addGood') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is adding new good to his store.")
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    db.addNewGood(callback_query.from_user.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.all()[0])
    await bot.send_message(chat_id=callback_query.message.chat.id, text="""<b>Отправьте, пожалуйста, название товара:</b>\n Внимание!\n Начав создавать товар, вы обязаны заполнить все поля до конца достоверной информацией. \n В противном случае карточка товара будет содержать всякую хуйню.""", parse_mode="html", reply_markup=None)

@dp.callback_query_handler(lambda c: c.data == 'storeSettings') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is setting his store.")
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    tokenInfo = db.getTokenInfoByOwnerId(callback_query.from_user.id)
    storeTransactions = db.getAllStoreTransactionsByID(callback_query.from_user.id)
    goods = db.getAllStoreGoodsByID(callback_query.from_user.id)
    currencyTransactionRank = db.getCurrencyTransactionRating().index(callback_query.from_user.id)
    totalAmount = sum([ transaction[5] for transaction in storeTransactions])
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f"""
    <b>Дневная выручка</b>: {totalAmount}
    <b>Количество покупок</b>: {len(storeTransactions)}
    <b>Количество товаров</b>:  {len(goods)}
    <b>Место по транзакциям</b>: {currencyTransactionRank}
    """,  parse_mode="html", reply_markup=kb.storeSettings)

@dp.callback_query_handler(lambda c: c.data == 'start' or c.data == "backToMenu") 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} started the bot.")
    if (not len(db.findUserById(callback_query.from_user.id))):
        db.createNewUser(str(callback_query.from_user.id), str(callback_query.from_user.username))
        db.createNewWallet(str(callback_query.from_user.id))
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)

@dp.callback_query_handler(lambda c: c.data == 'cabinet')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered cabinet.")
    
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    cabinetKB = InlineKeyboardMarkup(row_width=3)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.row(inline_btn_5, inline_btn_6, inline_btn_7)
        cabinetKB.row(kb.inline_btn_8)
    else:
        cabinetKB.row(inline_btn_5)
        cabinetKB.row(kb.inline_btn_8)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Добро пожаловать в ваш личный кабинет", reply_markup=cabinetKB)

@dp.callback_query_handler(lambda c: c.data == 'store')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered store.")
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Нинада ломать бота я вижу тебя, {callback_query.from_user.username}", reply_markup=kb.testKB)

@dp.callback_query_handler(lambda c: c.data == 'tradeBtn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered exchange section.")
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Нинада ломать бота я вижу тебя, {callback_query.from_user.username}", reply_markup=kb.testKB)

@dp.callback_query_handler(lambda c: c.data == 'myToken')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is looking at his token.")
    await bot.answer_callback_query(callback_query.id)
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    tokenInfo = db.getTokenInfoByOwnerId(callback_query.from_user.id)
    rating = db.getCurrenciesOwnerIDsRating().index(callback_query.from_user.id)+1
    information = f"""
<b>Вся информация по вашему личному токену.</b>


<b>Название:</b> {tokenInfo[5]} {tokenInfo[1]}
<b>Эквивалент в кекекоинах:</b> {tokenInfo[2]}
<b>Количество транзакций за сегодня:</b> {tokenInfo[3]}
<b>Место в рейтинге самых дорогих монет:</b> {rating}
    """
    await bot.send_photo(callback_query.message.chat.id, photo=open(tokenInfo[6], 'rb'), caption=information, parse_mode="html", reply_markup=cabinetKB)

@dp.callback_query_handler(lambda c: c.data == 'balance')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is checking his balance.")
    await bot.answer_callback_query(callback_query.id)
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    coins = db.getAllCtyprosNamesAndEmojis()
    balanceData = ""
    for coin in coins:
        balanceData += coin[1] + coin[0] + ": " + str(db.getCurrentAmountOfCurrencyByUserId(coin[0], callback_query.from_user.id)) + "\n"
    await bot.send_message(chat_id=callback_query.message.chat.id, text=
    f"""
    <b>Ваш баланс составляет:</b>
    <b>______________________</b>


{balanceData}
    

    В общей сложности это составляет 0 Кекекоинов.
    """, parse_mode="html", reply_markup=cabinetKB)

###Команды
@dp.message_handler(commands=['checkId'])
async def send_welcome(message: types.Message):
    print(message.from_user.id)
    await message.answer(
        """
        ok
    """,
    )

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