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

@bp_v1.route('/user', methods=["GET","POST"])
async def userPost(request):
    if request.method == "GET":
        logger.info('request server from path /user GET method')
        return json({
            "testSQLData": SqlApiV1Obj.test(2)
        })
    elif request.method == "POST":
        logger.info('request server from path /user POST method')
        body_data_byte = request.body.decode('utf-8')
        data = jsonobj.loads(body_data_byte)
        return json({
            "parsed": True,
            "url": request.url,
            "query_string": request.query_string,
            "args": request.args,
            "query_args": request.query_args,
            "body_byte": body_data_byte,
            "body_json": data,
            "dict_key": list(data.keys()),
            "endpoint": request.endpoint,
            "testSQLData": SqlApiV1Obj.test(2)
        })
    