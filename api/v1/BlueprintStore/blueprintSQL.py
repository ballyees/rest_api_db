from sanic import Blueprint
from sanic.response import json, stream
from .SQLite import SqlApiV1Obj
from ..Tokenize import TokenizerUser
from ..loggingFile import Logger

bp_v1 = Blueprint('v1', url_prefix='/api/store', version="v1")

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
