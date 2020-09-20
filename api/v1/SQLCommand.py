class SQLCommand():
    @staticmethod
    def getUser(username):
        # return f"""SELECT * FROM users WHERE username={username}"""
        return f"""SELECT * FROM users"""
    @staticmethod
    def insertUser(user):
        return f"""INSERT INTO users VALUES ('{user['username']}', '{user['hashedPassword']}', '{user['salt']}')"""