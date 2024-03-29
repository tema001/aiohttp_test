from aiohttp import web
from aiohttp.web_request import Request

from products.application.query import ProductQuery
from products.application.commands import ProductCommand

from products.infra.repository import ProductRepository
from db import get_session

from shared.utils import json_response


router = web.RouteTableDef()


@router.get('/category/{category_name}/products')
async def get_product_by_category(request: Request):
    query = ProductQuery(ProductRepository(), get_session)
    product_id = request.match_info['category_name']
    result = await query.get_products(product_id)

    return json_response(result)


@router.get('/product/{product_id}')
async def get_product(request: Request):
    query = ProductQuery(ProductRepository(), get_session)
    product_id = request.match_info['product_id']
    result = await query.get_product(product_id)

    if not result:
        raise web.HTTPNotFound

    return json_response(result)


@router.put('/product')
async def new_product(request: Request):
    command = ProductCommand(ProductRepository(), get_session)
    body = await request.json()
    p_id = await command.create_new(body)

    return web.Response(body=str(p_id), status=201)


@router.delete('/product/{product_id}')
async def delete_product(request: Request):
    command = ProductCommand(ProductRepository(), get_session)
    product_id = request.match_info['product_id']
    await command.delete(product_id)

    return web.Response(status=204)

