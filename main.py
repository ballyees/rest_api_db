from sanic import Sanic
from api.v1.BlueprintUser.blueprintSQL import bp_v1
from api.v1.Tokenize import TokenizerUser, TokenizerAdmin
from time import sleep

app = Sanic('projectDB')

app.blueprint(bp_v1)

if __name__ == "__main__":
    try:
        TokenizerUser.loadToken()
        TokenizerAdmin.loadToken()
        app.run(host="127.0.0.1", port=8000, auto_reload=True)
    except KeyboardInterrupt as e:
        print(e)
        
        print('server stop with admin')
        TokenizerUser.storeToken()
        TokenizerAdmin.storeToken()
        sleep(5)
        print('end process')
    finally:
        pass
