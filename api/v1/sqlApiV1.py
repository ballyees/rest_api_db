import sqlite3
from os.path import join, dirname, abspath

class SqlApiV1:
    def __init__(self, DBName):
        self.__PathDB = join(dirname(abspath(__file__)), DBName)
        # self.__PathDB = join('\\'.join(dirname(abspath(__file__)).split('\\')[:-1]), DBName)
        self.__connector = sqlite3.connect(self.__PathDB)
        self.__DBName = DBName
        self.__cur = self.__connector.cursor()

    async def closeDB(self, saveData=True):
        if saveData:
            self.__connector.commit()
        self.__connector.close()
        
    def getConnector(self):
        return  self.__connector
    
    def getDBName(self):
        return self.__DBName
    
    def getCursor(self):
        return self.__cur

    def changeDB(self, DBName, savePreviousDB):
        self.closeDB(savePreviousDB)
        self.__connector = sqlite3.connect(DBName)

