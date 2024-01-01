from aiohttp.web import HTTPConflict, HTTPNotFound

from typing import Mapping, Callable, AsyncContextManager
from uuid import UUID

from ..infra.repository import ProductRepository
from ..schemas import ProductCreate


class SuchProductAlreadyExist(HTTPConflict):
    ...


class ProductCommand:

    def __init__(self,
                 repo: ProductRepository,
                 db_session: Callable[[], AsyncContextManager[...]]):
        self.repo = repo
        self.db_session = db_session

    async def create_new(self, body: Mapping) -> UUID:
        async with self.db_session() as session:
            res = await self.repo.search_duplicate(session, body['category_id'], body['product_name'])
            if res:
                raise SuchProductAlreadyExist

            product = ProductCreate(**body)
            await self.repo.add_new(session, product)
            await self.repo.commit(session)

            return product.id

    async def delete(self, product_id: str):
        async with self.db_session() as session:
            res = await self.repo.delete(session, product_id)
            if res == 0:
                raise HTTPNotFound(text='No such product')

            await self.repo.commit(session)
