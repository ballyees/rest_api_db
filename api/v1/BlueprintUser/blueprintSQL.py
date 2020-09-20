from sanic import Blueprint
from sanic.response import json, text
from .SQLite import SqlApiV1Obj
from sanic.log import logger
from .Tokenize import Tokenizer


bp_v1 = Blueprint('v1', url_prefix='/api', version="v1")

@bp_v1.listener('after_server_stop')
async def close_connection(app, loop):
    logger.info('close server')
    await SqlApiV1Obj.close()

@bp_v1.route('/user/<username>', methods=["GET"])
async def userGET(request, username):
    logger.info('request server from path /user GET method')
    if not request.headers.get('token', None):
        return json({'exception': 'Authentication Failed', 'code': 1, 'description': 'none token'}, status=401) 
    elif Tokenizer.checkTokenAndUsername(request.headers['token'], username):
        return json({
            "responseData": SqlApiV1Obj.getUser(username)
        })
    elif not Tokenizer.checkToken(request.headers['token']):
        return json({'exception': 'Authentication Failed', 'code': 2, 'description': 'wrong token'}, status=401)
    else:
        return json({'exception': 'Authentication Failed', 'code': 3, 'description': 'permission deined'}, status=401)
            
@bp_v1.route('/user', methods=["POST"])
async def userPost(request):
    logger.info('request server from path /user POST method')
    data = request.json
    if not Tokenizer.addSocketIp(request.socket):
        return json({
            "detail": SqlApiV1Obj.insertUser(data)
        })
    else:
        return json({'exception': 'to many request to server'}, status=401)

@bp_v1.route('/user/login', methods=["POST"])
async def userLogin(request):
    data = request.json
    responseLogin = await SqlApiV1Obj.loginAuthentication(data)
    if responseLogin['Success']:
        return json({
            "responseData": responseLogin["responseData"],
            "token": Tokenizer.generateToken(data['username'])
        })
    else:
        return json(responseLogin)