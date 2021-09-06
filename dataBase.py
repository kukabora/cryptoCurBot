import sqlite3
class DB:

    dbName = 'database.db'

    def __init__(self):
        pass

    def getBotToken(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from tokens")
        result = self.cursor.fetchone()[1]
        self.connection.close()
        return result

    def createNewUser(self, id, username):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into users (id, username) values ({id}, '{username}')")
        self.connection.commit()
        self.connection.close()

    def findUserById(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from users where id = {id}")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def createNewWallet(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into wallets (wallet_owner) values ({id})")
        self.connection.commit()
        self.connection.close()

    def getWalletBuyUserId(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from wallets where wallet_owner = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result

    def checkIsTokenOwner(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select token_owner from users where id = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]
    
    def getCurrentAmountOfCurrencyByUserId(self, currency, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select {currency} from wallets where wallet_owner = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

    def updateWalletAmountOf(self, currency, value, id):
        previousAmount = self.getCurrentAmountOfCurrencyByUserId(currency, id)
        newAmount = previousAmount + value
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"update wallets set {currency} = {newAmount} where wallet_owner = {id}")
        self.connection.commit()
        self.connection.close()

    def getAllCtyprosNamesAndEmojis(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute("select name, smile from cryptos")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def getTokenInfoByOwnerId(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from cryptos where ownerId = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result

    def getCurrenciesOwnerIDsRating(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select ownerId from cryptos order by kekPrice ASC")
        result = [ownerId[0] for ownerId in self.cursor.fetchall()]
        self.connection.close()
        return result

    def getAllStoreTransactionsByID(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from transactions where recieverId = {id} AND fromStore = 1")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def getAllStoreGoodsByID(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from goods where ownerId = {id}")
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def getCurrencyTransactionRating(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select ownerId from cryptos order by kekPrice ASC")
        result = [ownerId[0] for ownerId in self.cursor.fetchall()]
        self.connection.close()
        return result
    
    def getCryptoNameById(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select name from cryptos where id = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

    def createNewTransaction(self, senderId, recieverId, currencyId, fromStore, amount):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into transactions (senderId, recieverId, currencyId, fromStore, amount) VALUES ({senderId}, {recieverId}, {currencyId}, {fromStore}, {amount})")
        self.connection.commit()
        self.connection.close()

    def addNewGood(self, id):
        cryptoData = self.getTokenInfoByOwnerId(id)
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into goods (ownerId, currency) values ({id}, {cryptoData[0]})")
        self.connection.commit()

    def getTheLastAddedGood(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from goods where ownerId = {id} order by id DESC")
        result = self.cursor.fetchone()
        self.connection.close()
        return result

    def updateGoodInfo(self, id, attr, value):
        lastGoodId = self.getTheLastAddedGood(id)[0]
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"update goods set {attr} = {value} where ownerId = {id} and id = {lastGoodId}")
        self.connection.commit()
        self.connection.close()
    
    def deleteGood(self, id):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"delete from goods where id = {id}")
        self.connection.commit()
        self.connection.close()
    
    def getAllUsers(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from users")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def getCurrencyIdByName(self, name):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select id from cryptos where name = '{name}'")
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

# db = DB()
# print([el[0] for el in db.getAllStoreGoodsByID(546535523)])

# db = DB()
# print(db.getCurrentAmountOfCurrencyByUserId("бАбАнОкОиН".casefold().capitalize(), 546535523))


# 546535523