import datetime

from aiohttp import web
from aiohttp.web_request import Request


router = web.RouteTableDef()


@router.get('/ws')
async def ws_example(request: Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        message = await ws.receive()
        if message.type == web.WSMsgType.TEXT:
            time = datetime.datetime.now().isoformat()
            await ws.send_str(f'{time} {message.data}')
        elif message.type == web.WSMsgType.CLOSE:
            print('closing')
            await ws.close()
            break
