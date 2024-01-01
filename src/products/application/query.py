from typing import Mapping, Callable, AsyncContextManager

from ..infra.repository import ProductRepository


class ProductQuery:

    def __init__(self,
                 repo: ProductRepository,
                 db_session: Callable[[], AsyncContextManager[...]]):
        self.repo = repo
        self.db_session = db_session

    async def get_product(self, product_id: str) -> Mapping | None:
        async with self.db_session() as session:
            res = await self.repo.get_by_id(session, product_id)
            await self.repo.commit(session)

            return res
