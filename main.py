from sanic import Sanic
from api.v1.blueprintSQL import bp_v1

app = Sanic(__name__)
app.blueprint(bp_v1)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, auto_reload=True)