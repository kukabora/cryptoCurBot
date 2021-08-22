class DB:
    import sqlite3


    dbName = ""
    tableName = ""


    def __init__(self):
        import sqlite3
        self.dbName = 'database.db'
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        print("successfully connected to the database")

    def getFirstRow(self, tableName):
        self.cursor.execute(f"select * from {tableName}")
        return self.cursor.fetchone()[1]