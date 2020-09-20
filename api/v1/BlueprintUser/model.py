import uuid, hashlib
class User():
    def __init__(self, username: str, password: str, token=None):
        self.__username = str(username)
        self.__salt = self.__getNewSalt()
        self.__password = password
        self.__hashedPassword = User.getNewHashingPassword(password, self.__salt)
        self.__token = token

    @staticmethod
    def getNewHashingPassword(password, salt):
        return hashlib.sha1(str(password).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()

    def __getNewSalt(self):
        return uuid.uuid4().hex

    def getUserJson(self):
        return {'username': self.__username, 'hashedPassword': self.__hashedPassword, 'salt': self.__salt, 'token': self.__token}

    def checkIsUser(self):
        return not ((not self.__username) | (not self.__password))

    def __str__(self):
        return f'username: {self.__username}, password: {self.__hashedPassword}, token: {self.__token}'

    def NewSalt(self):
        self.__salt = self.__getNewSalt()
        self.__hashedPassword = User.getNewHashingPassword(self.__password, self.__salt)


# user1 = User('123', 'asldkj1l2kjlajlsd')
# user2 = User('123', 'asldkj1l2kjlajlsd')
# print(User.checkIsUser(user1, user2))