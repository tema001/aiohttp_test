from typing import Mapping

from sqlalchemy import select, insert, delete, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.repository import GenericRepository

from model import Product, Category

from ..schemas import ProductCreate


class ProductRepository(GenericRepository):

    async def commit(self, session: AsyncSession):
        await session.commit()

    async def get_by_id(self, session: AsyncSession, _id: str) -> Mapping | None:
        stmt = select(Product.id, Product.product_name, Product.price, Category.category_name) \
            .join(Category).where(Product.id == _id)

        res = await session.execute(stmt)
        res = res.mappings().one_or_none()

        if res:
            return {**res}

    async def search_duplicate(self, session: AsyncSession,
                               category_id: str,
                               product_name: str) -> UUID | None:
        stmt = select(Product.id)\
                .where(Product.product_name == product_name, Product.category_id == category_id)
        res = await session.execute(stmt)

        return res.scalar_one_or_none()

    async def add_new(self, session: AsyncSession, product: ProductCreate):
        stmt = insert(Product).values(product_id=product.id, product_name=product.product_name,
                                      price=product.price, category_id=product.category_id)

        await session.execute(stmt)

    async def delete(self, session: AsyncSession, _id: str) -> int:
        stmt = delete(Product).where(Product.id == _id)
        res = await session.execute(stmt)
        return res.rowcount

    async def get_many_by_category_name(self, session: AsyncSession, category_name: str):
        sub_stmt = select(Category.category_id).where(Category.category_name == category_name).scalar_subquery()
        stmt = select(Product.id, Product.product_name, Product.price).where(Product.category_id == sub_stmt)

        res = await session.execute(stmt)
        return res.mappings().all()
