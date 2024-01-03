from aiohttp import web
from aiohttp.web_request import Request

from api.routers.products import router as product_router
from api.routers.ws import router as ws_router

from db import init

router = web.RouteTableDef()


@router.get('/')
async def hello(request: Request):
    return web.Response(text="Hello, world")


app = web.Application()

app.on_startup.append(init)
app.add_routes(router)
app.add_routes(product_router)
app.add_routes(ws_router)

web.run_app(app)
