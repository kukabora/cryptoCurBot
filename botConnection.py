import logging
from dataBase import DB
import keyboards as kb

from aiogram import Bot, Dispatcher, executor, types

db = DB()

API_TOKEN = db.getFirstRow("tokens")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

###Кнопки
@dp.callback_query_handler(lambda c: c.data == 'start' or c.data == "backToMenu") 
async def process_callback_button1(callback_query: types.CallbackQuery):
    if (not len(db.findUserById(callback_query.from_user.id))):
        db.createNewUser(str(callback_query.from_user.id))
        db.createNewWallet(str(callback_query.from_user.id))
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="С чего начнём?", reply_markup=kb.inline_kb2)

@dp.callback_query_handler(lambda c: c.data == 'cabinet')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Добро пожаловать в ваш личный кабинет", reply_markup=kb.cabinetKB)

@dp.callback_query_handler(lambda c: c.data == 'store')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Какую валюту вы бы хотели использовать при покупке?", reply_markup=kb.buyKB)

@dp.callback_query_handler(lambda c: c.data == 'tradeBtn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Вы отдаете: ", reply_markup=kb.trade1KB)

@dp.callback_query_handler(lambda c: c.data == 'balance')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    balance = db.getWalletBuyUserId(callback_query.from_user.id)
    
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=
    f"""
    Ваш баланс составляет:
    🐥Бабанокоин: ({balance[2]})
    Мнепохуйтокен: ({balance[3]})
    Гослингкоин: ({balance[4]})
    РэдДублон: ({balance[5]})
    Попакоин: ({balance[6]})
    👾Душнилатокин: ({balance[7]})
    🕷паааакоин): ({balance[8]})
    💊Туринариум: ({balance[9]})
    Чак-Чак: ({balance[10]})
    🦽ДохлаяМонета: ({balance[11]})
    """, reply_markup=kb.cabinetKB)

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