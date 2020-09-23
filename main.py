from sanic import Sanic
from api.v1.BlueprintUser.blueprintSQL import bp_v1
from api.v1.Tokenize import TokenizerUser, TokenizerAdmin
from time import sleep

app = Sanic('projectDB')

app.blueprint(bp_v1)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    try:
        TokenizerUser.loadToken()
        TokenizerAdmin.loadToken()
        # app.run(host=host, port=port, auto_reload=True)
        app.run(host=host, port=port)
    except Exception as e:
        print(e)
        print('Server Stopped with admin')
        TokenizerUser.storeToken()
        TokenizerAdmin.storeToken()
        print('end process')
    # finally:
    #     pass
