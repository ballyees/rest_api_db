import sqlite3
from os.path import join, dirname, abspath
class SqlApiV1():
    def __init__(self, DBName):
        self.__PathDB = join(dirname(abspath(__file__)), DBName)
        self.__connector = sqlite3.connect(self.__PathDB)
        self.__DBName = DBName
        self.__cur = self.__connector.cursor()

    def closeDB(self, saveData=True):
        if saveData:
            self.__connector.commit()    
        self.__connector.close()
        
    def getConnector(self):
        return  self.__connector

    def changeDB(self, DBName, savePreviousDB):
        self.closeDB(savePreviousDB)
        self.__connector = sqlite3.connect(DBName)

    def test(self, LimitRow=None):
        Limit = ''
        if LimitRow is not None:
            Limit = f'LIMIT {LimitRow}'
        sql_cmd = f'''
                    SELECT SOH.CustomerID, C.FirstName, C.MiddleName, C.LastName, SOH.TotalDue
                    FROM SalesOrderHeader as SOH, Customer as C
                    WHERE SOH.CustomerID=C.CustomerID
                    {Limit}
            '''
        rows = self.__cur.execute(sql_cmd)
        col = []
        for c in self.__cur.description:
            col.append(c[0])
        return [dict(zip(col, row)) for row in rows.fetchall()]

SqlApiV1Obj = SqlApiV1('lab2.db')
