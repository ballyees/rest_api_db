from api.v1.Tokenize import TokenizerUser, TokenizerAdmin
TokenizerUser.clearAllToken()
TokenizerAdmin.clearAllToken()
TokenizerUser.storeToken()
TokenizerAdmin.storeToken()