from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from db.settings import settings

engine = create_async_engine(url=settings.db_url, echo=settings.db_echo)

AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with AsyncSession() as session:
        yield session
