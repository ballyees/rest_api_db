class Configure:
    def __init__(self):
        
        # config Tokenizer
        self.keyLoadStoreToken = 'token'
        self.keyLoadStoreTokenStart = 'tokenStart'
        self.keyLoadStoreTokenEnd = 'tokenEnd'
        self.keyLoadStoreTokenName = 'name'
        self.DateFormat = '%Y-%m-%dT%H:%M:%S.%f' #iso 8601 format
        self.keyLoadStoreData = 'data'
        self.keyLoadStoreDateFormat = 'fmt'

        # config request and response :: user blueprint
        self.keyTokenHeader = 'tokenAuthenticate'
        self.keyRefreshToken = 'refreshToken'
        self.keyRequestUsername = 'username'
        self.keyRequestPassword = 'password'
        self.keyResponseData = 'responseData'
        self.keyResponseLoginType = {'Admin': 'Admin',
        'President': 'President',
        'VP Sales': 'VP Sales',
        'VP Marketing': 'VP Marketing',
        'Sales Manager (APAC)': 'Sales Manager',
        'Sales Manager (EMEA)': 'Sales Manager',
        'Sales Manager (NA)': 'Sales Manager',
        'Sales Rep': 'Sales'
        }
        self.keyRequestHeaderLogoutType = 'type'

        # config query sql :: user blueprint
        self.keyQueryUsersUsername = 'username'
        self.keyQueryUsersHashedPassword = 'hashedPassword'
        self.keyQueryUsersSalt = 'salt'
        self.keyQueryUsersType = 'type'
        
ConfigureAPI = Configure()