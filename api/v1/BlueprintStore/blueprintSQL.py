from sanic import Blueprint
from sanic.response import json, stream
from .SQLite import SqlApiV1Obj
from ..Tokenize import TokenizerUser
from ..loggingFile import Logger
from ..configure import ConfigureAPI


bp_v1_store = Blueprint('v1', url_prefix='/api/store', version="v1")

@bp_v1_store.listener('after_server_stop')
async def close_connection(app, loop):
    await SqlApiV1Obj.close()

@bp_v1_store.route('/<officeCode>', methods=["GET"])
async def userGET(request, officeCode):
    if not request.headers.get(ConfigureAPI.keyTokenHeader, None):
        Logger.write(f'IP {request.socket} [no token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 1, 'description': 'none token'}, status=401) 
    elif TokenizerUser.checkTokenAndName(request.headers['token'], officeCode):
        Logger.write(f'IP {request.socket} [{officeCode} query data]', 'request-data')
        res = SqlApiV1Obj.getUser(officeCode)
        del res[0]['salt']
        return json({
            "responseData": res
        })
    elif not TokenizerUser.checkToken(request.headers[ConfigureAPI.keyTokenHeader]):
        Logger.write(f'IP {request.socket} [unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 2, 'description': 'wrong token'}, status=401)
    else:
        Logger.write(f'IP {request.socket[0]} [{officeCode} use unknown token]', 'request-data')
        return json({'exception': 'Authentication Failed', 'code': 3, 'description': 'permission deined'}, status=401)
            
@bp_v1_store.route('/', methods=["POST"])
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
