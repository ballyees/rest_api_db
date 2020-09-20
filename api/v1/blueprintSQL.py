from sanic import Blueprint
from sanic.response import json, text
from .SQLite import SqlApiV1Obj
from sanic.log import logger
import json as jsonobj

bp_v1 = Blueprint('v1', url_prefix='/api', version="v1")

@bp_v1.listener('after_server_stop')
async def close_connection(app, loop):
    logger.info('close server')
    await SqlApiV1Obj.close()

@bp_v1.route('/', methods=["GET"])
async def api_v1_root(request):
    logger.info('request server from path /')
    return json({'hello': 'is my api'})

@bp_v1.route('/user/<username>', methods=["GET"])
async def userGET(request, username):
        logger.info('request server from path /user GET method')
        return json({
            "userData": SqlApiV1Obj.getUser(username)
        })  

@bp_v1.route('/user', methods=["POST"])
async def userPost(request):
    logger.info('request server from path /user POST method')
    body_data_byte = request.body.decode('utf-8')
    data = jsonobj.loads(body_data_byte)
    return json({
        "Success": SqlApiV1Obj.insertUser(data)
    })