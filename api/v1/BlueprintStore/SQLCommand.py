class SQLCommand:
    @staticmethod
    def getUser(username):
        return f"""SELECT * FROM users WHERE username like '{username}'"""
    
    @staticmethod
    def getUserAll():
        return f"""SELECT * FROM users"""
        
    @staticmethod
    def insertUser(user, typeData='common'):
        return f"""INSERT INTO users (username, hashedPassword, salt, type) VALUES ('{user['username']}', '{user['hashedPassword']}', '{user['salt']}', '{typeData}')"""