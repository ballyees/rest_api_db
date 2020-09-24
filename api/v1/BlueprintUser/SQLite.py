import sqlite3
from os.path import join, dirname, abspath
from .SQLCommand import SQLCommand
from ..model import User
from ..sqlApiV1 import SqlApiV1

class SqlApiUserV1(SqlApiV1):
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
            del data['password']
            return {'Success': True, 'user': data}

    def insertUserFake(self, data):
        if self.getUser(data['username']):
            return {'Success': False, 'code': 'we have username'}
        else:
            user = User(data['username'], data['password'])
            if not user.checkIsUser():
                return {'Success': False, 'code': 'no username or password'}
            self.__cur.execute(SQLCommand.insertUserFake(user.getUserJson()))
            self.__connector.commit()
            return {'Success': True}

    async def loginAuthentication(self, data):
        user = self.getUser(data['username'])
        if len(user) == 1:
            user = user[0]
            hashed = User.getNewHashingPassword(data['password'], user['salt'])
            if user['hashedPassword'] == hashed:
                return {'Success': True, 'responseData': [user]}
            else:
                return {'Success': False, 'exception': 'Wrong password'}
        else:
            return {'Success': False, 'exception': 'Wrong username'}

SqlApiV1Obj = SqlApiUserV1('loginModel.db')
