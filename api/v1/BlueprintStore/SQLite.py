import sqlite3
from os.path import join, dirname, abspath
from .SQLCommand import SQLCommand
from ..model import User
from ..sqlApiV1 import SqlApiV1

class SqlApiStoreV1(SqlApiV1):
    def __init__(self, DBName):
        SqlApiV1.__init__(self, DBName)
        self.__connect = self.getConnector()
        self.__cur = self.getCursor()
        
    def getUser(self, username):
        sql_cmd = SQLCommand.getUser(username)
        rows = self.__cur.execute(sql_cmd)
        col = []
        for c in self.__cur.description:
            col.append(c[0])
        return [dict(zip(col, row)) for row in rows.fetchall()]
    
    def insertUser(self, data):
        if self.getUser(data['username']):
            return {'Success': False, 'code': 'we have username'}
        else:
            user = User(data['username'], data['password'])
            if not user.checkIsUser():
                return {'Success': False, 'code': 'no username or password'}
            self.__cur.execute(SQLCommand.insertUser(user.getUserJson(), data['type']))
            self.__connector.commit()
            return {'Success': True}

SqlApiV1Obj = SqlApiStoreV1('loginModel.db')
