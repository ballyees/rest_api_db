import hashlib, uuid
from datetime import datetime as dt, timedelta
from random import random
from os.path import join, dirname, abspath
from json import dump, load

class Token:
    def __init__(self, name='', timeout=9999, data={}):
        if data:
            self.__name = data['name']
            self.__dt = dt.strptime(data['tokenStart'], data['fmt'])
            self.__timeout = dt.strptime(data['tokenEnd'], data['fmt'])
            self.__token = data['token']
            self.__isTimeout = False
            self.tokensIsExpired()
        else:
            self.__name = name
            self.__dt = dt.now()
            self.__timeout = self.__dt + timedelta(seconds=timeout)
            self.__token = self.__generateToken()
            self.__isTimeout = False
    
    def __generateToken(self):
        Token = hashlib.sha224(str(f'{random()}_access_{self.__name}').encode('utf-8') + str(uuid.uuid4().hex).encode('utf-8')).hexdigest()
        return Token

    def tokensIsExpired(self):
        isTimeout = dt.now() >= self.__timeout
        self.__setTimeout(isTimeout)
        return isTimeout
    
    def getIsTimeout(self):
        return self.__isTimeout
    
    def tokenIsName(self, name):
        return self.__name == name

    def __setTimeout(self, isTimeout):
        self.__isTimeout = isTimeout

    def getToken(self):
        return self.__token
    
    def getJsonToken(self, fmt):
        return {'token': self.__token, 'name': self.__name, 'tokenStart': self.__dt.strftime(fmt), 'tokenEnd': self.__timeout.strftime(fmt)}

    def __str__(self):
        return f'{self.__name}: {self.__token}'

class TokenizeAndMiddleWare:
    def __init__(self, filename='Token', Type='', limitRequest=1000000, limitRequestSec=2, timeout=9999):
        self.__filename = f"{filename}_{Type}.json"
        self.__filePath = join(join(dirname(abspath(__file__)), 'token'), self.__filename)
        self.__type = Type
        self.__tokens = {}
        self.__socketIp = {}
        self.__limitRequest = limitRequest
        self.__limitRequestSec = limitRequestSec
        self.__timeout = timeout
        self.__fmt = '%Y-%m-%dT%H:%M:%S.%f' #iso 8601 format
    
    def loadToken(self):
        print(f'loading {self.__type} Token')
        with open(self.__filePath, 'r') as jsonFile:
            jsonToken = load(jsonFile)['data']
            for t in jsonToken:
                token = Token(data=t)
                if not token.getIsTimeout():
                    self.__tokens[token.getToken()] = token

    def storeToken(self):
        with open(self.__filePath, 'w') as file:
            jsonToken = {}
            jsonToken['data'] = []
            for t in self.__tokens:
                if not t.tokensIsExpired():
                    jsonToken['data'].append(t.getJsonToken(self.__fmt))
            dump(jsonToken, file)

    async def generateAndAddToken(self, name):
        token = Token(name, self.__timeout)
        self.__tokens[token.getToken()] = token
        return token.getToken()

    async def isLogin(self, name):
        for t in self.__tokens:
            print(self.__tokens[t])
            if self.__tokens[t].tokenIsName(name):
                return True
        return False

    def addSocketIp(self, socket):
        if socket[0] not in self.__socketIp:
            print(socket[0])
            self.__socketIp[socket[0]] = {}
            self.__socketIp[socket[0]]['Time'] = []
            self.__socketIp[socket[0]]['Time'].append(dt.now())
            return False
        else:
            self.__socketIp[socket[0]]['Time'].append(dt.now())
            return self.checkBotWithSocket(socket)
    
    def checkBotWithSocket(self, socket):
        if len(self.__socketIp[socket[0]].get('Time', [])) > self.__limitRequest:
            if (self.__socketIp[socket[0]]['Time'][-1] - self.__socketIp[socket[0]]['Time'][0]).seconds < self.__limitRequestSec:
                return True
            else:
                self.__socketIp[socket[0]]['Time'].clear()
                return False
        return False

    def checkToken(self, Token=''):
        return Token in self.__tokens
    
    def checkTimeout(self, Token=''):
        tokenData = self.__tokens.get(Token, None)
        if tokenData:
            if tokenData.tokensIsExpired():
                self.delToken(Token)
                return True
            else:
                return False
        else:
            return False, 'None token'

    def checkTokenAndName(self, Token='', name=''):
        return (not self.checkTimeout(Token)) and (Token in self.__tokens) and self.__tokens[Token].tokenIsName(name)

    def delToken(self, Token=''):
        if self.__tokens.get(Token, None):
            del self.__tokens[Token]
            return True
        return False

TokenizerUser = TokenizeAndMiddleWare(Type='User')
TokenizerAdmin = TokenizeAndMiddleWare(Type='Admin')