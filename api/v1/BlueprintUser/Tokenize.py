import hashlib, uuid
from datetime import datetime as dt
class Tokenize():

    def __init__(self):
        self.__tokens = {}
        self.__socketIp = {}
        self.__limit = 2
        self.__timeSec = 2

    def generateToken(self, username):
        Token = hashlib.sha1(str(f'requst_{username}').encode('utf-8') + str(uuid.uuid4().hex).encode('utf-8')).hexdigest()
        self.__tokens[Token] = username
        return Token

    def addSocketIp(self, socket):
        if socket[0] not in self.__socketIp:
            self.__socketIp[socket[0]]['Time'] = []
            self.__socketIp[socket[0]]['Time'].append(dt.now())
            return False
        else:
            self.__socketIp[socket[0]]['Time'].append(dt.now())
            return self.checkBotWithSocket(self.__socketIp[socket[0]])
    
    def checkBotWithSocket(self, socket):
        if len(self.__socketIp[socket[0]].get('Time', [])) > self.__limit:
            if (self.__socketIp[socket[0]]['Time'][-1] - self.__socketIp[socket[0]]['Time'][0]).seconds < self.__timeSec:
                return True
            else:
                self.__socketIp[socket[0]]['Time'].clear()
                return False
        return False

    def checkToken(self, Token=''):
        return Token in self.__tokens
    
    def checkTokenAndUsername(self, Token='', username=''):
        return (Token in self.__tokens) and (self.__tokens[Token] == username)

    def delToken(self, Token=''):
        if Token in self.__tokens:
            del self.__tokens[Token]
            return True
        return False

Tokenizer = Tokenize()