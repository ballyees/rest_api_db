from sanic import Blueprint
from sanic.response import json, stream
from .SQLite import SqlApiV1Obj
from ..Tokenize import TokenizerUser
from ..loggingFile import Logger

bp_v1 = Blueprint('v1', url_prefix='/api/user', version="v1")

@bp_v1.listener('after_server_stop')
async def close_connection(app, loop):
    await SqlApiV1Obj.close()

@bp_v1.route('/<username>', methods=["GET"])
async def userGET(request, username):
    if not request.headers.get('token', None):
        Logger.write(f'IP {request.socket} [no token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 1, 'description': 'none token'}, status=401) 
    elif TokenizerUser.checkTokenAndName(request.headers['token'], username):
        Logger.write(f'IP {request.socket} [{username} query data]', 'request-data')
        res = SqlApiV1Obj.getUser(username)
        del res[0]['salt']
        return json({
            "responseData": res
        })
    elif not TokenizerUser.checkToken(request.headers['token']):
        Logger.write(f'IP {request.socket} [unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 2, 'description': 'wrong token'}, status=401)
    else:
        Logger.write(f'IP {request.socket[0]} [{username} use unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 3, 'description': 'permission deined'}, status=401)
            
@bp_v1.route('/', methods=["POST"])
async def userPost(request):
    data = request.json
    if not TokenizerUser.addSocketIp(request.socket):
        data['type'] = 'Common'
        res = SqlApiV1Obj.insertUser(data)
        if res['Success']:
            Logger.write(f'IP {request.socket[0]} [create {data["username"]} successful]', 'create')
        else:
            Logger.write(f'IP {request.socket[0]} [create {data["username"]} cannot successful]', 'create')
        return json({
                "detail": res
            })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} to many request to server]', 'create')
        return json({'exception': 'to many request to server'}, status=401)

@bp_v1.route('/login', methods=["POST"])
async def userLogin(request):
    data = request.json
    if await TokenizerUser.isLogin(data['username']):
        return json({"Success": False, 'exception': 'username is login'})
    responseLogin = await SqlApiV1Obj.loginAuthentication(data)
    if responseLogin['Success']:
        Logger.write(f'IP {request.socket[0]} [{data["username"]} login to server successful]', 'Login')
        del responseLogin["responseData"][0]['salt']
        return json({
            "responseData": responseLogin["responseData"],
            "token": await TokenizerUser.generateAndAddToken(data['username'])
        })
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} try login to server]', 'Login')
        return json(responseLogin)

@bp_v1.route('/loguot', methods=["POST"])
async def userLogout(request):
    if not request.headers.get('token', None):
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} cannot send token]', 'logout')
        return json({'Success': False})
    elif TokenizerUser.delToken(request.headers['token']):
        Logger.write(f'IP {request.socket[0]} [{data["username"]} logout successful]', 'logout')
        return json({'Success': True})
    else:
        Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} cannot find token]', 'logout')
        return json({'Success': False})

# @bp_v1.route('/fakeUser', methods=["POST"])
# async def userPostFake(request):
#     data = request.json
#     if not TokenizerUser.addSocketIp(request.socket):
#         data['type'] = 'Common'
#         res = SqlApiV1Obj.insertUserFake(data)
#         if res['Success']:
#             Logger.write(f'IP {request.socket[0]} [create {data["username"]} successful]', 'create')
#         else:
#             Logger.write(f'IP {request.socket[0]} [create {data["username"]} cannot successful]', 'create')
#         return json({
#                 "detail": res
#             })
#     else:
#         Logger.write(f'IP {request.socket[0]} [{data.get("username", "Unknown")} to many request to server]', 'create')
#         return json({'exception': 'to many request to server'}, status=401)