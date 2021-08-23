class DB:
    import sqlite3

    dbName = 'database.db'

    def __init__(self):
        pass

    def getFirstRow(self, tableName):
        import sqlite3
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from {tableName}")
        result = self.cursor.fetchone()[1]
        self.connection.close()
        return result

    def createNewUser(self, id, username):
        import sqlite3
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into users (id, username) values ({id}, '{username}')")
        self.connection.commit()
        self.connection.close()

    def findUserById(self, id):
        import sqlite3
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from users where id = {id}")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def createNewWallet(self, id):
        import sqlite3
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"insert into wallets (wallet_owner) values ({id})")
        self.connection.commit()
        self.connection.close()

    def getWalletBuyUserId(self, id):
        import sqlite3
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from wallets where wallet_owner = {id}")
        result = self.cursor.fetchone()
        self.connection.close()
        return result