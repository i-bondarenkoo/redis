import crud
from db.redis_client import redis
from schemas.singer import CreateSinger
from sqlalchemy.ext.asyncio import AsyncSession
from services.helpers import convert_orm_to_dict
import json

CACHE_TIME = 60


async def create_singer_and_cache(singer_in: CreateSinger, session: AsyncSession):
    singer = await crud.create_singer_crud(singer_in=singer_in, session=session)
    singer_to_dict: dict = convert_orm_to_dict(singer)
    key = f"singer:{singer.id}"
    await redis.set(key, json.dumps(singer_to_dict), ex=CACHE_TIME)
    print("Сохранили объект в Redis")
    return singer
