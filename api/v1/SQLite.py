import sqlite3
import os
class SqlApiV1():
    def __init__(self, DBName):
        self.__PathDB = os.path.join(os.path.dirname(os.path.abspath(__file__)), DBName)
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
