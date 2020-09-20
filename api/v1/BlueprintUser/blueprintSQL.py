from sanic import Blueprint
from sanic.response import json, text
from .SQLite import SqlApiV1Obj
from .Tokenize import Tokenizer
from ..loggingFile import Logger

bp_v1 = Blueprint('v1', url_prefix='/api', version="v1")

@bp_v1.listener('after_server_stop')
async def close_connection(app, loop):
    await SqlApiV1Obj.close()

@bp_v1.route('/user/<username>', methods=["GET"])
async def userGET(request, username):
    if not request.headers.get('token', None):
        Logger.write(f'IP {request.socket} [no token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 1, 'description': 'none token'}, status=401) 
    elif Tokenizer.checkTokenAndUsername(request.headers['token'], username):
        Logger.write(f'IP {request.socket} [{username} query data]', 'request-data')
        return json({
            "responseData": SqlApiV1Obj.getUser(username)
        })
    elif not Tokenizer.checkToken(request.headers['token']):
        Logger.write(f'IP {request.socket} [unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 2, 'description': 'wrong token'}, status=401)
    else:
        Logger.write(f'IP {request.socket[0]} [{username} use unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 3, 'description': 'permission deined'}, status=401)
            
@bp_v1.route('/user', methods=["POST"])
async def userPost(request):
    data = request.json
    if not Tokenizer.addSocketIp(request.socket):
        Logger.write(f'IP {request.socket[0]} [create {data["username"]} successful]', 'create')
        return json({
            "detail": SqlApiV1Obj.insertUser(data)
        })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} to many request to server]', 'create')
        return json({'exception': 'to many request to server'}, status=401)

@bp_v1.route('/user/login', methods=["POST"])
async def userLogin(request):
    data = request.json
    responseLogin = await SqlApiV1Obj.loginAuthentication(data)
    if responseLogin['Success']:
        Logger.write(f'IP {request.socket[0]} [{data["username"]} login to server successful]', 'Login')
        return json({
            "responseData": responseLogin["responseData"],
            "token": Tokenizer.generateToken(data['username'])
        })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} try login to server]', 'Login')
        return json(responseLogin)

@bp_v1.route('/user/loguot', methods=["POST"])
async def userLogout(request):
    if not request.headers.get('token', None):
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} can not send token]', 'logout')
        return json({'Success': False})
    elif Tokenizer.delToken(request.headers['token']):
        Logger.write(f'IP {request.socket[0]} [{data["username"]} logout successful]', 'logout')
        return json({'Success': True})
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} can not find token]', 'logout')
        return json({'Success': False})
