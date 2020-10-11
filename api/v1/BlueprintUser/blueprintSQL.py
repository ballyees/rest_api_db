from sanic import Blueprint
from sanic.response import json, stream
from .SQLite import SqlApiV1Obj
from ..Tokenize import TokenizerUser, TokenizerAdmin
from ..loggingFile import Logger
from ..configure import ConfigureAPI
bp_v1_user = Blueprint('user_v1', url_prefix='/api/user', version="v1")

@bp_v1_user.listener('after_server_stop')
async def close_connection(app, loop):
    await SqlApiV1Obj.closeDB()

async def addRefreshToken(res, token):
    ref = TokenizerAdmin.refreshToken(token)
    if ref[0]:
        res[ConfigureAPI.keyRefreshToken] = ref[1]
    return res

@bp_v1_user.route('/<username>', methods=["GET"])
async def userGET(request, username):
    if not request.headers.get(ConfigureAPI.keyTokenHeader, None):
        Logger.write(f'IP {request.socket} [no token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 1, 'description': 'none token'}, status=401) 
    elif await TokenizerUser.checkTokenAndName(request.headers[ConfigureAPI.keyTokenHeader], username):
        Logger.write(f'IP {request.socket} [{username} query data]', 'request-data')
        res = SqlApiV1Obj.getUser(username)
        del res[0]['salt']
        return json({
            ConfigureAPI.keyResponseData: res
        })
    elif not await TokenizerUser.checkToken(request.headers[ConfigureAPI.keyTokenHeader]):
        Logger.write(f'IP {request.socket} [unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 2, 'description': 'wrong token'}, status=401)
    else:
        Logger.write(f'IP {request.socket[0]} [{username} use unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 3, 'description': 'permission deined'}, status=401)
            
@bp_v1_user.route('/', methods=["POST"])
async def userPost(request):
    data = request.json
    if not await TokenizerAdmin.checkTokenAndName(data.get(ConfigureAPI.keyTokenHeader, ''), data.get(ConfigureAPI.keyRequestUsername, '')):
        data['type'] = 'Common'
        res = SqlApiV1Obj.insertUser(data)
        reponse = await addRefreshToken({ ConfigureAPI.keyResponseData: res }, data[ConfigureAPI.keyTokenHeader])
        if res['Success']:
            Logger.write(f'IP {request.socket[0]} [create {data[ConfigureAPI.keyRequestUsername]} successful]', 'create')
        else:
            Logger.write(f'IP {request.socket[0]} [create {data[ConfigureAPI.keyRequestUsername]} cannot successful]', 'create')
        return json(reponse)
    else:
        Logger.write(f'IP {request.socket[0]} request to server]', 'create')
        return json({'exception': 'permission denied'}, status=401)

@bp_v1_user.route('/login', methods=["POST"])
async def userLogin(request):
    data = request.json
    responseLogin = await SqlApiV1Obj.loginAuthentication(data)
    if responseLogin['Success']:
        Logger.write(f'IP {request.socket[0]} [{data[ConfigureAPI.keyRequestUsername]} login to server successful]', 'Login')
        del responseLogin[ConfigureAPI.keyResponseData][0][ConfigureAPI.keyQueryUsersSalt]
        responseData = responseLogin[ConfigureAPI.keyResponseData]
        if responseData[0][ConfigureAPI.keyQueryUsersType] == ConfigureAPI.keyResponseLoginType['Admin']:
            token = await TokenizerAdmin.generateAndCheckToken(data[ConfigureAPI.keyRequestUsername])
        else:
            token = await TokenizerUser.generateAndCheckToken(data[ConfigureAPI.keyRequestUsername])
        responseData[0][ConfigureAPI.keyRequestHeaderLogoutType] = ConfigureAPI.keyResponseLoginType[responseData[0][ConfigureAPI.keyQueryUsersType]]
        if ConfigureAPI.keyQueryUsersType != ConfigureAPI.keyRequestHeaderLogoutType:
            del responseData[0][ConfigureAPI.keyQueryUsersType]
        return json({
            ConfigureAPI.keyResponseData: responseData,
            ConfigureAPI.keyTokenHeader: token
        })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get(ConfigureAPI.keyRequestUsername, "Unknown")} try login to server]', 'Login')
        return json(responseLogin, status=400)

async def isLogout(typeUser, token):
    if typeUser == ConfigureAPI.keyResponseLoginType['Admin']:
        return await TokenizerAdmin.delToken(token) 
    else:
        return await TokenizerUser.delToken(token)

@bp_v1_user.route('/logout', methods=["POST"])
async def userLogout(request):
    if not request.headers.get(ConfigureAPI.keyTokenHeader, None) or not request.headers.get(ConfigureAPI.keyRequestHeaderLogoutType, None):
        Logger.write(f'IP {request.socket[0]} [cannot send token]', 'logout')
        return json({'Success': False}, status=400)
    elif await isLogout(request.headers[ConfigureAPI.keyRequestHeaderLogoutType], request.headers[ConfigureAPI.keyTokenHeader]):
        Logger.write(f'IP {request.socket[0]} [logout successful]', 'logout')
        return json({'Success': True})
    else:
        Logger.write(f'IP {request.socket[0]} [cannot find token]', 'logout')
        return json({'Success': False}, status=406)
