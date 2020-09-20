from sanic import Sanic
import json as jsonobj
from sanic.response import json, text
from api.v1.SQLite import SQLAPI_V1

name_sanic = "DBAPI"
app = Sanic(name_sanic)
SQLCon = SQLAPI_V1('lab2.db')

@app.route("/", methods=["GET"])
async def test(request):
    return json({"hello": "world"})

@app.route("/hello", methods=["POST"])
async def test2(request):
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
        "testSQLData": SQLCon.test(5)
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, auto_reload=True)