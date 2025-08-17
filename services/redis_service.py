import crud
from db.redis_client import redis
from schemas.singer import CreateSinger, UpdateSinger
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
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


async def get_singer_by_id_and_cache(singer_id: int, session: AsyncSession):
    key = f"singer:{singer_id}"
    cache = await redis.get(key)
    if cache:
        print("взяли данные из redis")
        data: dict = json.loads(cache)
        return data
    singer = await crud.get_singer_by_id_crud(singer_id=singer_id, session=session)
    if singer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Певец не найден"
        )
    print("Делаем запрос в БД и кэшируем в редис")
    save_to_redis: dict = convert_orm_to_dict(singer)
    await redis.set(key, json.dumps(save_to_redis), ex=CACHE_TIME)
    return singer


async def update_singer_and_cache(
    singer_in: UpdateSinger, singer_id: int, session: AsyncSession
):
    update_singer = await crud.update_singer_partial_crud(
        singer_in=singer_in, singer_id=singer_id, session=session
    )
    key = f"singer:{singer_id}"

    print("Сохраняем данные в редис")
    data = convert_orm_to_dict(update_singer)
    await redis.set(key, json.dumps(data), ex=CACHE_TIME)
    return update_singer


async def delete_singer_and_cache(singer_id: int, session: AsyncSession):
    singer = await crud.delete_singer_crud(singer_id=singer_id, session=session)
    if singer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Певец не найден"
        )
    else:
        key = f"singer:{singer_id}"
        await redis.delete(key)
        print("Удалили запись из кэша редис")
    return singer
