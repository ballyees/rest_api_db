from sanic import Sanic
from api.v1.BlueprintUser.blueprintSQL import bp_v1_user
from api.v1.Tokenize import TokenizerUser, TokenizerAdmin
from time import sleep
import asyncio

app = Sanic('projectDB')

app.blueprint(bp_v1_user)

async def loadToken():
    await asyncio.gather(TokenizerUser.loadToken(), TokenizerAdmin.loadToken())

async def storeToken():
    await asyncio.gather(TokenizerUser.storeToken(), TokenizerAdmin.storeToken())

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    try:
        print('---- [loading tokens] ----')
        asyncio.run(loadToken())
        app.run(host=host, port=port, auto_reload=True)
        raise Exception('Stop server')
    except (Exception, KeyboardInterrupt, SystemExit) as e:
        print(e)
        print('---- [store tokens] ----')
        asyncio.run(storeToken())
        print('---- [end process] ----')
