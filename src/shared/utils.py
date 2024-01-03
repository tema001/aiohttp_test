import json
from typing import Mapping

from aiohttp import web


def json_response(body: Mapping, status: int = 200):
    res = json.dumps(body, default=str, allow_nan=False)
    return web.Response(status=status, body=res, content_type='application/json')