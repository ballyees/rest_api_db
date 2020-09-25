from sanic import Blueprint
from sanic.response import json, stream
from .SQLite import SqlApiV1Obj
from ..Tokenize import TokenizerUser
from ..loggingFile import Logger
from ..configure import ConfigureAPI
bp_v1_user = Blueprint('v1', url_prefix='/api/user', version="v1")

@bp_v1_user.listener('after_server_stop')
async def close_connection(app, loop):
    await SqlApiV1Obj.closeDB()

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
    if not await TokenizerUser.addSocketIp(request.socket):
        data['type'] = 'Common'
        res = SqlApiV1Obj.insertUser(data)
        if res['Success']:
            Logger.write(f'IP {request.socket[0]} [create {data[ConfigureAPI.keyRequestUsername]} successful]', 'create')
        else:
            Logger.write(f'IP {request.socket[0]} [create {data[ConfigureAPI.keyRequestUsername]} cannot successful]', 'create')
        return json({
                ConfigureAPI.keyResponseData: res
            })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get(ConfigureAPI.keyRequestUsername, "Unknown")} to many request to server]', 'create')
        return json({'exception': 'to many request to server'}, status=401)

@bp_v1_user.route('/login', methods=["POST"])
async def userLogin(request):
    data = request.json
    responseLogin = await SqlApiV1Obj.loginAuthentication(data)
    if responseLogin['Success']:
        Logger.write(f'IP {request.socket[0]} [{data[ConfigureAPI.keyRequestUsername]} login to server successful]', 'Login')
        del responseLogin[ConfigureAPI.keyResponseData][0]['salt']
        return json({
            ConfigureAPI.keyResponseData: responseLogin[ConfigureAPI.keyResponseData],
            ConfigureAPI.keyTokenHeader: await TokenizerUser.generateAndCheckToken(data[ConfigureAPI.keyRequestUsername])
        })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get(ConfigureAPI.keyRequestUsername, "Unknown")} try login to server]', 'Login')
        return json(responseLogin)

@bp_v1_user.route('/logout', methods=["POST"])
async def userLogout(request):
    data = request.json
    if not request.headers.get(ConfigureAPI.keyTokenHeader, None):
        Logger.write(f'IP {request.socket[0]} [{data.get(ConfigureAPI.keyRequestUsername, "Unknown")} cannot send token]', 'logout')
        return json({'Success': False})
    elif await TokenizerUser.delToken(request.headers[ConfigureAPI.keyTokenHeader]):
        Logger.write(f'IP {request.socket[0]} [{data[ConfigureAPI.keyRequestUsername]} logout successful]', 'logout')
        return json({'Success': True})
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get(ConfigureAPI.keyRequestUsername, "Unknown")} cannot find token]', 'logout')
        return json({'Success': False})
