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

# db = DB()
# if db.checkIsTokenOwner(505350250):
#     print("owner")
# else:
#     print("not owner")