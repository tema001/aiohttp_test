from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from contextlib import asynccontextmanager

db_name = 'aaadb'
user = 'postgres'
password = '1234'
domain = 'localhost'

DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{domain}:5432/{db_name}'
engine = create_async_engine(DATABASE_URL, echo=True)
SessionInst = async_sessionmaker(bind=engine)

Base = declarative_base()


async def init(app):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with SessionInst() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
