import logging
from dataBase import DB

from aiogram import Bot, Dispatcher, executor, types

db = DB()

API_TOKEN = db.getFirstRow("tokens")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

