import logging
from dataBase import DB
import keyboards as kb
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
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

def makeTransactionBetweenUsers(senderId, recieverId, currencyId, fromStore, amount):
    db.createNewTransaction(senderId, recieverId, currencyId, fromStore, amount)
    currencyName = db.getCryptoNameById(currencyId)
    db.updateWalletAmountOf(currencyName, -amount, senderId)
    db.updateWalletAmountOf(currencyName, amount, recieverId)

TestStates = States()
###Хэндлеры состояний
@dp.message_handler(state=TestStates.all()[13])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        stateData = await state.get_data()
        if message.text == "✔Да":
            db.updateWalletAmountOf(db.getCryptoNameById(stateData['currency1']), -float(stateData['amount']), message.from_user.id)
            db.updateWalletAmountOf(db.getCryptoNameById(stateData['currency2']), float(stateData['newAmount']), message.from_user.id)
            await state.reset_state()
            await message.answer(text=f"Вы успешно конвертировали <b>{stateData['amount']} {db.getCryptoNameById(stateData['currency1'])}ов</b> в <b>{stateData['newAmount']} {db.getCryptoNameById(stateData['currency2'])}ов.</b>\n<b><u>Балансы:</u></b>\n{db.getCryptoNameById(stateData['currency1'])}:{db.getCurrentAmountOfCurrencyByUserId(db.getCryptoNameById(stateData['currency1']), message.from_user.id)}\n{db.getCryptoNameById(stateData['currency2'])}:{db.getCurrentAmountOfCurrencyByUserId(db.getCryptoNameById(stateData['currency2']), message.from_user.id)}", parse_mode="html", reply_markup=ReplyKeyboardRemove())
            await message.answer(text="Чем займемся далее?", reply_markup=kb.inline_kb2)
        elif message.text == "❌Нет":
            await state.set_state(TestStates.all()[12])
            kbd = ReplyKeyboardMarkup().row(KeyboardButton("◀️Назад"))
            await message.answer(text=f"Введите количество {db.getCryptoNameById(stateData['currency1'])}ов которое вы бы хотели конвертировать в {db.getCryptoNameById(stateData['currency2'])}ы.", reply_markup=kbd)
        else:
            await message.answer("У тебя было 3 кнопки и ты все равно решил вписать ответ своими руками. Я в шоке.")

@dp.message_handler(state=TestStates.all()[12])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        if re.match(r'^-?\d+(?:\.\d+)$', message.text) or message.text.isdigit():
            stateData = await state.get_data()
            if float(message.text) <= db.getCurrentAmountOfCurrencyByUserId(db.getCryptoNameById(stateData['currency1']), message.from_user.id):
                await state.update_data(data={"amount":float(message.text)})
                await state.set_state(TestStates.all()[13])

                kbd = ReplyKeyboardMarkup()
                kbd.row(KeyboardButton("✔Да"), KeyboardButton("❌Нет"))
                kbd.row(KeyboardButton("◀️Назад"))
                
                acceptableAmount = float(message.text)*(db.getCryptoCoefficientById(stateData['currency2'])/db.getCryptoCoefficientById(stateData['currency1']))
                await state.update_data(data={'newAmount':acceptableAmount})
                await message.answer(text=f"При конвертации <b>{message.text}</b> <b>{db.getCryptoNameById(stateData['currency1'])}ов</b> в <b>{db.getCryptoNameById(stateData['currency2'])}ы</b>, вы получите <b><u>{acceptableAmount}</u></b> <b>{db.getCryptoNameById(stateData['currency2'])}ов</b>.\n\nПодтвердить обмен валют?", parse_mode="html", reply_markup=kbd)
            else:
                await message.answer(text=f"У вас недостаточно средств для совершения обмена валютами.\n Всего на балансе <b>{db.getCryptoNameById(stateData['currency1'])}ов</b>: {db.getCurrentAmountOfCurrencyByUserId(db.getCryptoNameById(stateData['currency1']), message.from_user.id)}", parse_mode="html")
        else:
            await message.answer("Неверное количество.")


@dp.message_handler(state=TestStates.all()[11])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        message.text = message.text[1:]
        if message.text in [coin[0] for coin in db.getAllCtyprosNamesAndEmojis()]:
            await state.update_data(data={"currency2":db.getCurrencyIdByName(message.text)})
            stateData = await state.get_data()
            await state.set_state(TestStates.all()[12])
            kbd = ReplyKeyboardMarkup().row(KeyboardButton("◀️Назад"))
            await message.answer(text=f"Введите количество {db.getCryptoNameById(stateData['currency1'])}ов которое вы бы хотели конвертировать в {db.getCryptoNameById(stateData['currency2'])}ы.", reply_markup=kbd)
        else:
            await state.set_state(TestStates.all()[12])
            kbd = ReplyKeyboardMarkup().row(KeyboardButton("◀️Назад"))
            await message.answer(text=f"Введите количество <b>{db.getCryptoNameById(stateData['currency1'])}ов</b> которое вы бы хотели конвертировать в <b>{db.getCryptoNameById(stateData['currency2'])}ы</b>.", parse_mode="html", reply_markup=kbd)
            await message.answer(text="Нет валюты с таким названием", reply_markup=kbd)
            

@dp.message_handler(state=TestStates.all()[10])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        message.text = message.text[1:]
        if message.text in [coin[0] for coin in db.getAllCtyprosNamesAndEmojis()]:
            await state.update_data(data={"currency1":db.getCurrencyIdByName(message.text)})
            stateData = await state.get_data()
            cryptosInfo = db.getAllCryptosInfo()
            info = f"На какую бы валюту вы хотели обменять свои {(message.text)}'ы?\n<b><u>ВНИМАНИЕ!!!\nВЫБИРАЙТЕ ТУ ВАЛЮТУ, КОТОРУЮ ВЫ БЫ ХОТЕЛИ ПОЛУЧИТЬ В ПРОЦЕССЕ ОБМЕНА!</u></b>\n\n"
            exchangeKbd = ReplyKeyboardMarkup()
            for i in range(len(cryptosInfo)):
                if cryptosInfo[i][0] == stateData['currency1']:
                    continue
                btn = KeyboardButton(f"{cryptosInfo[i][5]}{cryptosInfo[i][1]}")
                exchangeKbd.row(btn)
                info += f"<b>Валюта: </b> {cryptosInfo[i][5]}{cryptosInfo[i][1]}\n"
                info += f"<b>Эквивалент в 1 кекекоине:</b> {cryptosInfo[i][2]} {cryptosInfo[i][1]}'ов\n"
                if i!=len(cryptosInfo)-1:
                    info += "--------------\n"
            exchangeKbd.row(KeyboardButton("◀️Назад"))
            await state.set_state(TestStates.all()[11])
            await bot.send_message(chat_id=message.chat.id, text=info, parse_mode="html", reply_markup=exchangeKbd)
        else:
            await message.answer(f"Нет криптовалюты с таким названием")


@dp.message_handler(state=TestStates.all()[9])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        if message.text == "✔Да":
            stateData = await state.get_data()
            if db.getCurrentAmountOfCurrencyByUserId(stateData['cryptoData'][1], message.from_user.id) >= int(stateData['goodInfo'][2]):
                makeTransactionBetweenUsers(message.from_user.id, stateData['storeId'], stateData['cryptoData'][0], 1, stateData['goodInfo'][2])
                await bot.send_message(stateData['storeId'], f"Пользователь <b>{message.from_user.username}</b> купил у вас товар под номером {stateData['goodInfo'][0]}({stateData['goodInfo'][1]}) за {stateData['goodInfo'][2]} {stateData['cryptoData'][1]}'ов.\n\n<b>Текущий баланс: </b>{db.getCurrentAmountOfCurrencyByUserId(stateData['cryptoData'][1], stateData['storeId'])}", parse_mode="html")
                await message.answer("Покупка успешна!", reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
                await state.reset_state()
            else:
                await message.answer("У тебя денег не хватает, бичуган ебаный.")
        elif message.text == "❌Нет":
            await state.set_state(TestStates.all()[7])
            stateData = await state.get_data()
            cryptoData = stateData['cryptoData']
            await state.update_data(data={"storeId": int(cryptoData[4])})
            info = f"Добро пожаловать в магазин пользователя <b>{db.findUserById(int(stateData['storeId']))[0][1]}</b>: \nЗдесь все приобритается за <b>{cryptoData[1]}</b>\n\n<b><u>ТОВАРЫ:</u></b>\n"
            goodsInfo = db.getAllStoreGoodsByID(int(cryptoData[4]))
            marketKB = ReplyKeyboardMarkup()
            for i in range(len(goodsInfo)):
                info += f"<b>Id:</b> {goodsInfo[i][0]}\n"
                info += f"<b>Название:</b> {goodsInfo[i][1]}\n"
                if i != len(goodsInfo)-1:
                    info += "-----------\n"
                marketKB.add(KeyboardButton(str(goodsInfo[i][0]) + " | " + str(goodsInfo[i][1])))
            info += "\n Выберите ID товара, который хотите приобрести:"
            marketKB.row(kb.cancelButton)
            await state.set_state(TestStates.all()[8])
            await message.answer(info, parse_mode="html", reply_markup=marketKB)
        else:
            await message.answer("Ты вообще че за хуйню вписал. У тебя было всего 3 кнопки сука и ты не смог из них выбрать ни одну?????? Ты в порядке?")


@dp.message_handler(state=TestStates.all()[8])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        messageData = message.text.split(' ')
        stateData = await state.get_data()
        if int(messageData[0]) in [int(good[0]) for good in db.getAllStoreGoodsByID(stateData['storeId'])]:
            await state.update_data(data={"goodId":int(messageData[0])})
            goodInfo = db.getGoodInfoById(int(messageData[0]))
            await state.update_data(data={"goodInfo":goodInfo})
            await state.set_state(TestStates.all()[9])
            info = f"<b>ID:</b>{goodInfo[0]}\n"
            info += f"<b>Название:</b>{goodInfo[1]}\n"
            info += f"<b>Цена:</b>{goodInfo[2]} {db.getCryptoNameById(goodInfo[3])}\n"
            info += f"<b>Продавец:</b>{db.findUserById(goodInfo[4])[0][1]}\n"
            info += f"<b>Описание:</b>{goodInfo[5]}\n"
            info += "----------------\nВы точно хотите купить этот товар?"
            goodKB = ReplyKeyboardMarkup().row(KeyboardButton("✔Да"), KeyboardButton("❌Нет"))
            goodKB.row(kb.cancelButton)
            await message.answer(info, parse_mode="html", reply_markup=goodKB)
        else:
            await message.answer("Нет такого товара в этом магазине.")

@dp.message_handler(state=TestStates.all()[7])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "◀️Назад":
        await state.reset_state()
        await bot.send_message(chat_id=message.chat.id, text="Возвращаем Вас в главное меню!", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)
    else:
        message.text = message.text[1:]
        if (message.text in [crypto[1] for crypto in db.getAllCryptosInfo()]):
            cryptoData = db.getCryptoInfoByName(message.text)
            await state.update_data(data={"storeId": int(cryptoData[4])})
            await state.update_data(data={"cryptoData": db.getCryptoInfoByName(message.text)})
            await state.set_state(TestStates.all()[8])
            info = f"Добро пожаловать в магазин пользователя <b>{db.findUserById(int(cryptoData[4]))[0][1]}</b>: \nЗдесь все приобритается за <b>{message.text}</b>\n\n<b><u>ТОВАРЫ:</u></b>\n"
            goodsInfo = db.getAllStoreGoodsByID(int(cryptoData[4]))
            marketKB = ReplyKeyboardMarkup()
            for i in range(len(goodsInfo)):
                info += f"<b>Id:</b> {goodsInfo[i][0]}\n"
                info += f"<b>Название:</b> {goodsInfo[i][1]}\n"
                info += f"<b>Цена: </b>{goodsInfo[i][2]}"
                if i != len(goodsInfo)-1:
                    info += "-----------\n"
                marketKB.add(KeyboardButton(str(goodsInfo[i][0]) + " | " + str(goodsInfo[i][1])))
            info += "\n Выберите ID товара, который хотите приобрести:"
            marketKB.row(kb.cancelButton)
            await state.set_state(TestStates.all()[8])
            await message.answer(info, parse_mode="html", reply_markup=marketKB)
        else:
            print("Нет такого магазина.")



@dp.message_handler(state=TestStates.all()[6])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    user_data = await state.get_data()
    if message.text.isdigit():
        if db.getCurrentAmountOfCurrencyByUserId(user_data['currency'], message.from_user.id) < int(message.text):
            await message.answer(f"У тебя столько нету.\nНа данный момент валюты '{user_data['currency'].capitalize()}' у тебя всего лишь {db.getCurrentAmountOfCurrencyByUserId(user_data['currency'].capitalize(), message.from_user.id)}", reply_markup=ReplyKeyboardRemove())
        elif int(message.text) < 0:
            await message.answer("Ты даун)")
        else:
            inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
            cabinetKB = InlineKeyboardMarkup(row_width=3)
            transactionBtn = InlineKeyboardButton('Переводы', callback_data='currencySendRecieve')
            if db.checkIsTokenOwner(message.from_user.id):
                inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
                inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
                cabinetKB.row(inline_btn_5, inline_btn_6, inline_btn_7, transactionBtn)
                cabinetKB.row(kb.inline_btn_8)
            else:
                cabinetKB.row(inline_btn_5, transactionBtn)
                cabinetKB.row(kb.inline_btn_8)
            if (int(message.text) > 0):
                makeTransactionBetweenUsers(message.from_user.id, user_data['recieverId'], db.getCurrencyIdByName(user_data['currency']), 0, int(message.text))
                await message.answer(f"Перевод успешно произведен!", reply_markup=cabinetKB)
                await bot.send_message(user_data['recieverId'], text=f"Пользователь {message.from_user.username} перевел вам {message.text} {user_data['currency']}\nТекущий баланс: <b>{db.getCurrentAmountOfCurrencyByUserId(user_data['currency'], user_data['recieverId'])}</b>", parse_mode="html")
            else:
                await state.reset_state()
                await message.answer(f"Перевод успешно отменен.", reply_markup=cabinetKB)
    else:
        await message.answer(f"Ммм. и че блять мне перевести ему {message.text} {user_data['currency']}'ов???\nНапиши блять нормально цифрами количество, которое хочешь ему перевести.", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=TestStates.all()[5])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    message.text = message.text[1:]
    if message.text.casefold() in [coin[0].casefold() for coin in db.getAllCtyprosNamesAndEmojis()]:
        await state.set_state(TestStates.all()[6])

        await state.update_data(data={"currency":message.text.casefold().capitalize()})

        await message.answer(f"Введите количество валюты, которое хотите перевести этому пользователю: \n Введите 0 чтобы отменить перевод.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Нет криптовалюты с таким названием")
        
@dp.message_handler(state=TestStates.all()[4])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text.split(' ')[0].isdigit():
        if int(message.text.split(' ')[0]) in [info[0] for info in  db.getAllUsers()]:
            await state.set_state(TestStates.all()[5])

            await state.update_data(data={"recieverId":int(message.text.split(' ')[0])})

            info = "В какой валюте вы бы хотели сделать перевод?\n"
            keyBoard = ReplyKeyboardMarkup()
            for currency in db.getAllCtyprosNamesAndEmojis():
                info += currency[1] + currency[0] + ": " + str(db.getCurrentAmountOfCurrencyByUserId(currency[0], message.from_user.id)) + "\n"
                btn = KeyboardButton(str(currency[1]+currency[0]))
                keyBoard.row(btn)
            info += "Введите название криптовалюты, в которой вы бы хотели осуществить перевод"
            await message.answer(info, reply_markup=keyBoard)
        else:
            await message.answer(f"Нет пользователя с таким айди")
    else:
        await message.answer(f"Напишите ID пользователя. Цифрами. Напишите. ID.", reply=False)

@dp.message_handler(state=TestStates.all()[3])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text.isdigit():
        if int(message.text) in [el[0] for el in db.getAllStoreGoodsByID(message.from_user.id)]:
            await state.reset_state()
            db.deleteGood(message.text)
            await message.answer(f"Товар успешно удалён!", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f"Хитрожопый дохуя? У тебя нет товара с таким айди")

    else:
        await message.answer(f"Цифрами блять напиши ID, что непонятного?", reply=False)

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
    await message.answer(f"Отправьте, пожалуйста, цену товара в своей валюте ({tokenInfo[1]}):", reply_markup=ReplyKeyboardRemove())

###Кнопки
@dp.callback_query_handler(lambda c: c.data == 'currencySendRecieve') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is going to make a money transaction.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    info = "Доступные для перевода пользователи:\n\n"
    allUsersInfo = db.getAllUsers()
    keyBoard = ReplyKeyboardMarkup()
    for i in range(len(allUsersInfo)):
        if str(allUsersInfo[i][0]) == str(callback_query.from_user.id):
            continue
        btn = KeyboardButton(str(allUsersInfo[i][0]) + " - " + str(allUsersInfo[i][1]))
        keyBoard.row(btn)
        info += f"""
<b>ID:</b>{allUsersInfo[i][0]}
<b>Username:</b>{allUsersInfo[i][1]}
        """
        if i != len(allUsersInfo) - 1:
            info += "-----------\n"
    info += "\n Введите айди пользователя, которому хотите совершить перевод:"
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.all()[4])
    await bot.send_message(chat_id=callback_query.message.chat.id, text=info, parse_mode="html", reply_markup=keyBoard)

@dp.callback_query_handler(lambda c: c.data == 'storePreview') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is looking at his store preview.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    goodsInfo = db.getAllStoreGoodsByID(callback_query.from_user.id)
    marketKB = InlineKeyboardMarkup()
    ownerUsername = callback_query.from_user.username
    tokenData = db.getTokenInfoByOwnerId(callback_query.from_user.id)
    backBtn = InlineKeyboardButton("Назад", callback_data="storeSettings")
    info = f"<b>Добро пожаловать в магазин пользователя {ownerUsername}: </b>\nЗдесь все приобритается за {tokenData[1]}"
    for i in range(len(goodsInfo)):
        info += f"<b>Id:</b> {goodsInfo[i][0]}\n"
        info += f"<b>Название:</b> {goodsInfo[i][1]}\n"
        info += f"<b>Цена:</b> {goodsInfo[i][2]}\n"
        info += f"<b>Описание:</b> {goodsInfo[i][5]}\n"
        if i != len(goodsInfo)-1:
            info += "-----------\n"
        marketKB.add(InlineKeyboardButton(str(goodsInfo[i][0]), callback_data="storeSettings"))
    info += "\n Выберите ID товара, который хотите приобрести:"
    marketKB.row(backBtn)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=info, parse_mode="html", reply_markup=marketKB)

@dp.callback_query_handler(lambda c: c.data == 'delGood') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is deleting single good in his store.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.all()[3])
    goodsInfo = db.getAllStoreGoodsByID(callback_query.from_user.id)
    info = "<b>Введите айди товара, который хотите удалить: </b>\n"
    for i in range(len(goodsInfo)):
        info += f"<b>Id:</b> {goodsInfo[i][0]}\n"
        info += f"<b>Название:</b> {goodsInfo[i][1]}\n"
        info += f"<b>Цена:</b> {goodsInfo[i][2]}\n"
        info += f"<b>Описание:</b> {goodsInfo[i][5]}\n"
        if i != len(goodsInfo)-1:
            info += "-----------\n"
    await bot.send_message(chat_id=callback_query.message.chat.id, text=info, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(lambda c: c.data == 'addGood') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is adding new good to his store.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    db.addNewGood(callback_query.from_user.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.all()[0])
    await bot.send_message(chat_id=callback_query.message.chat.id, text="""<b>Отправьте, пожалуйста, название товара:</b>\n Внимание!\n Начав создавать товар, вы обязаны заполнить все поля до конца достоверной информацией. \n В противном случае карточка товара будет содержать всякую хуйню.""", parse_mode="html", reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(lambda c: c.data == 'storeSettings') 
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is setting his store.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
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
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except MessageCantBeDeleted:
        pass
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="С чего начнём?", reply_markup=kb.inline_kb2)

@dp.callback_query_handler(lambda c: c.data == 'cabinet')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered cabinet.")
    
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    cabinetKB = InlineKeyboardMarkup(row_width=3)
    transactionBtn = InlineKeyboardButton('Переводы', callback_data='currencySendRecieve')
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.row(inline_btn_5, inline_btn_6, inline_btn_7, transactionBtn)
        cabinetKB.row(kb.inline_btn_8)
    else:
        cabinetKB.row(inline_btn_5, transactionBtn)
        cabinetKB.row(kb.inline_btn_8)
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Добро пожаловать в ваш личный кабинет", reply_markup=cabinetKB)

@dp.callback_query_handler(lambda c: c.data == 'store')
async def process_callback_button1(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    print(f"User {callback_query.from_user.username} entered store.")
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    info = "Какую криптовалюту вы бы хотели использовать при покупке?\n"
    storeKbd = ReplyKeyboardMarkup()
    currencies = db.getAllCryptosInfo()
    for i in range(len(currencies)):
        if currencies[i][4]==callback_query.from_user.id:
            continue
        info += "<b>Валюта:</b> " + currencies[i][5]+ currencies[i][1] + "\n<b>Количество товаров:</b> "  + str(len(db.getAllStoreGoodsByID(currencies[i][4]))) + "\n<b>Владелец:</b> " + str(db.findUserById(currencies[i][4])[0][1]) + "\n" 
        btn = KeyboardButton(text = str(currencies[i][5]) + str(currencies[i][1]))
        storeKbd.row(btn)
        if (i!=len(currencies)-1):
            info += "----------------\n"
    storeKbd.row(kb.cancelButton)
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(TestStates.all()[7])
    await bot.send_message(chat_id=callback_query.message.chat.id, text=info, parse_mode="html", reply_markup=storeKbd)

@dp.callback_query_handler(lambda c: c.data == 'tradeBtn')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} entered exchange section.")
    state = dp.current_state(user=callback_query.from_user.id)
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    await bot.answer_callback_query(callback_query.id)
    cryptosInfo = db.getAllCryptosInfo()
    info = "Какую бы валюту вы хотели обменять?\n<b><u>ВНИМАНИЕ!!!\nВЫБИРАЙТЕ ТУ ВАЛЮТУ, КОТОРУЮ ВЫ БЫ ХОТЕЛИ ОТДАТЬ!</u></b>\n\n"
    exchangeKbd = ReplyKeyboardMarkup()
    for i in range(len(cryptosInfo)):
        btn = KeyboardButton(f"{cryptosInfo[i][5]}{cryptosInfo[i][1]}")
        exchangeKbd.row(btn)
        info += f"<b>Валюта: </b> {cryptosInfo[i][5]}{cryptosInfo[i][1]}\n"
        info += f"<b>Эквивалент в 1 кекекоине:</b> {cryptosInfo[i][2]} {cryptosInfo[i][1]}'ов\n"
        if i!=len(cryptosInfo)-1:
            info += "--------------\n"
    exchangeKbd.row(KeyboardButton("◀️Назад"))
    await state.set_state(TestStates.all()[10])
    await bot.send_message(chat_id=callback_query.message.chat.id, text=info, parse_mode="html", reply_markup=exchangeKbd)

@dp.callback_query_handler(lambda c: c.data == 'myToken')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(f"User {callback_query.from_user.username} is looking at his token.")
    await bot.answer_callback_query(callback_query.id)
    inline_btn_5 = InlineKeyboardButton('Мой баланс', callback_data='balance')
    inline_btn_6 = InlineKeyboardButton('Мой магазин', callback_data='storeSettings')
    transactionBtn = InlineKeyboardButton('Переводы', callback_data='currencySendRecieve')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6, transactionBtn)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
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
    transactionBtn = InlineKeyboardButton('Переводы', callback_data='currencySendRecieve')
    cabinetKB = InlineKeyboardMarkup(row_width=3).add(inline_btn_5, inline_btn_6, transactionBtn)
    if db.checkIsTokenOwner(callback_query.from_user.id):
        inline_btn_7 = InlineKeyboardButton('Моя монетa', callback_data='myToken')
        cabinetKB.add(inline_btn_7, kb.inline_btn_8)
    else:
        cabinetKB.add(kb.inline_btn_8)
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        pass
    coins = db.getAllCtyprosNamesAndEmojis()
    balanceData = ""
    for coin in coins:
        balanceData += coin[1] + coin[0] + ": " + "<b>"+str(db.getCurrentAmountOfCurrencyByUserId(coin[0], callback_query.from_user.id)) + "</b>" + "\n"
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