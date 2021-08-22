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
@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Начать", reply_markup=kb.inline_kb1)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


###Команды
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply(
        """Привет!
    Я персональный кекестанский помощник по крипте!
    С моей помощью вы можете легко обменивать свои (и не только свои) токены
    а так же покупать за них различные услуги.
    
    Начнем?""",
    reply_markup=kb.inline_kb1
    )

###Всё остальное
@dp.message_handler()
async def nonExistingCommand(message: types.Message):
    if (message.text[0] == "/"):
        await message.answer("Нет такой команды. \nМне похуй.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)