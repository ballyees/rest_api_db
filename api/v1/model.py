import uuid, hashlib
class User():
    def __init__(self, username: str, password: str, token=None):
        self.__username = str(username)
        self.__salt = self.__getNewSalt()
        self.__password = password
        self.__hashedPassword = self.__getNewHashingPassword(password, self.__salt)
        self.__token = token

    def __getNewHashingPassword(self, password, salt):
        return hashlib.sha512(str(password).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()

    def __getNewSalt(self):
        return uuid.uuid4().hex

    def getUserJson(self):
        return {'username': self.__username, 'password': self.__hashedPassword, 'token': self.__token}

    @staticmethod
    def checkIsUser(user1, user2):
        print(f'user1: {user1}')
        print(f'user2: {user2}')
        return str(user1) == str(user2)

    def __str__(self):
        return f'username: {self.__username}, password: {self.__hashedPassword}, token: {self.__token}'

    def setSalt(self, salt):
        self.__salt = salt
        self.__hashedPassword = self.__getNewHashingPassword(self.__password, self.__salt)

    def getSalt(self):
        return self.__salt

user1 = User('123', 'asldkj1l2kjlajlsd')
user2 = User('123', 'asldkj1l2kjlajlsd')
user2.setSalt(user1.getSalt())
print(User.checkIsUser(user1, user2))