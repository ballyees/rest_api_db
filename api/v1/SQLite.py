import sqlite3
from os.path import join, dirname, abspath
from .SQLCommand import SQLCommand
from .loggingFile import Logger
from .model import User

class SqlApiV1():
    def __init__(self, DBName):
        self.__PathDB = join(dirname(abspath(__file__)), DBName)
        self.__connector = sqlite3.connect(self.__PathDB)
        self.__DBName = DBName
        self.__cur = self.__connector.cursor()

    async def closeDB(self, saveData=True):
        if saveData:
            self.__connector.commit()
        self.__connector.close()
        
    def getConnector(self):
        return  self.__connector

    def changeDB(self, DBName, savePreviousDB):
        self.closeDB(savePreviousDB)
        self.__connector = sqlite3.connect(DBName)

    def getUser(self, username):
        sql_cmd = SQLCommand.getUser(username)
        print(sql_cmd)
        rows = self.__cur.execute(sql_cmd)
        col = []
        for c in self.__cur.description:
            col.append(c[0])
        return [dict(zip(col, row)) for row in rows.fetchall()]
    
    def insertUser(self, data):
        if self.getUser(data['username']):
            return {'Sucess': False, 'code': 'have username'}
        else:
            user = User(data['username'], data['password'])
            self.__cur.execute(SQLCommand.insertUser(user.getUserJson()))
            self.__connector.commit()
            return 1
SqlApiV1Obj = SqlApiV1('classicmodels.sqlite')
