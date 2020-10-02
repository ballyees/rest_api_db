from sanic import Sanic
from api.v1.BlueprintUser.blueprintSQL import bp_v1_user
from api.v1.Tokenize import TokenizerUser, TokenizerAdmin
from time import sleep
from asyncio import run, gather

app = Sanic('projectDB')

app.blueprint(bp_v1_user)

async def loadToken():
    await gather(TokenizerUser.loadToken(), TokenizerAdmin.loadToken())

async def storeToken():
    await gather(TokenizerUser.storeToken(), TokenizerAdmin.storeToken())

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    try:
        print('---- [loading tokens] ----')
        run(loadToken())
        app.run(host=host, port=port, auto_reload=True)
        raise Exception('Stop server')
    except (Exception, KeyboardInterrupt, SystemExit) as e:
        print(e)
        print('---- [store tokens] ----')
        run(storeToken())
        print('---- [end process] ----')
