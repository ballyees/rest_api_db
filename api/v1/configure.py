class Configure:
    def __init__(self):
        self.keyTokenHeader = 'tokenAuthenticate'
        self.keyLoadStoreToken = 'token'
        self.keyLoadStoreTokenStart = 'tokenStart'
        self.keyLoadStoreTokenEnd = 'tokenEnd'
        self.keyLoadStoreTokenName = 'name'
        self.DateFormat = '%Y-%m-%dT%H:%M:%S.%f' #iso 8601 format
        self.keyLoadStoreData = 'data'
        self.keyLoadStoreDateFormat = 'fmt'
        self.keyRequestUsername = 'username'
        self.keyRequestPassword = 'password'
        self.keyResponseData = 'responseData'

ConfigureAPI = Configure()