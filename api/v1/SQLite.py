import sqlite3
import pandas as pd
import os
from collections import Counter
class SQLAPI_V1():
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
if __name__ == '__main__':
    SQLCon = SQLAPI_V1('lab2.db')
    con = SQLCon.getConnector()
    cnt = Counter()
    cur = con.cursor()
    sql_cmd = '''
                    SELECT SOH.CustomerID, C.FirstName, C.MiddleName, C.LastName, SOH.TotalDue
                    FROM SalesOrderHeader as SOH, Customer as C
                    WHERE SOH.CustomerID=C.CustomerID
            '''
    rows = cur.execute(sql_cmd)
    col = []
    for c in cur.description:
        col.append(c[0])
    rows_fetchall = [dict(zip(col, row)) for row in rows.fetchall()]
    df = pd.DataFrame(rows_fetchall.copy())
    rows_fetchall.clear()
    del rows_fetchall
    cnt = Counter(df['CustomerID'])
    filter_cus = list(filter(lambda cus: cnt[cus] == 1, cnt))
    del cnt
    print(df[df['CustomerID'].map(lambda cus: cus in filter_cus)])

    SQLCon.closeDB()
