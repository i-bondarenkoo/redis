import crud
from db.redis_client import redis
from schemas.singer import CreateSinger, UpdateSinger
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from services.helpers import convert_orm_to_dict
import json
import logging

CACHE_TIME = 180
# объект который будет писать логику из каждого отдельного файла
logger = logging.getLogger(__name__)


async def create_singer_and_cache(singer_in: CreateSinger, session: AsyncSession):
    singer = await crud.create_singer_crud(singer_in=singer_in, session=session)
    singer_to_dict: dict = convert_orm_to_dict(singer)
    key = f"singer:{singer.id}"
    await redis.set(key, json.dumps(singer_to_dict), ex=CACHE_TIME)
    logger.info(
        "Создали новый ORM-объект в таблице БД и кэшировали его в Redis",
    )
    await clear_cache()
    logger.info(
        "Очищаем key-value для списка в Redis, тк после изменения он мог устареть",
    )
    # print("Отчистили список объектов из кэша Redis")
    return singer


async def get_singer_by_id_and_cache(singer_id: int, session: AsyncSession):
    key = f"singer:{singer_id}"
    cache = await redis.get(key)
    if cache:
        logger.info(
            "GET-запрос на получение объекта по id, берем данные из Redis",
        )
        # print("взяли данные из redis")
        data: dict = json.loads(cache)
        return data
    singer = await crud.get_singer_by_id_crud(singer_id=singer_id, session=session)
    if singer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Певец не найден",
        )
    logger.info(
        "Кэш пустой, делаем запрос в БД и сохраняем в Redis",
    )
    # print("Делаем запрос в БД и кэшируем в редис")
    save_to_redis: dict = convert_orm_to_dict(singer)
    await redis.set(key, json.dumps(save_to_redis), ex=CACHE_TIME)
    return singer


async def get_list_singers_and_cache(
    session: AsyncSession,
    start: int = 0,
    stop: int = 3,
):
    key = f"singers:{start}:{stop}"
    cache = await redis.get(key)
    if cache:
        logger.info(
            "GET-запрос на получение списка объектов, берем данные из Redis",
        )
        # print("Берем данные для списка из Redis")
        data: list[dict] = json.loads(cache)
        return data
    singer = await crud.get_list_singer_crud(start=start, stop=stop, session=session)
    logger.info(
        "Кэш редис пустой, делаем запрос в БД и сохраняем результат в Redis",
    )
    # print("Сохраняем данные в Redis")
    save_to_redis: list[dict] = [convert_orm_to_dict(s) for s in singer]
    await redis.set(key, json.dumps(save_to_redis), ex=CACHE_TIME)
    return singer


async def update_singer_and_cache(
    singer_in: UpdateSinger, singer_id: int, session: AsyncSession
):
    update_singer = await crud.update_singer_partial_crud(
        singer_in=singer_in, singer_id=singer_id, session=session
    )
    key = f"singer:{singer_id}"
    logger.info(
        "PATCH-запрос, обновляем данные, перезаписываем/сохраняем данные после обновления в Redis",
    )
    # print("Сохраняем данные в редис")
    data = convert_orm_to_dict(update_singer)
    await redis.set(key, json.dumps(data), ex=CACHE_TIME)
    await clear_cache()
    logger.info(
        "Очищаем key-value для списка в Redis, тк после изменения он мог устареть",
    )
    # print("Обновили объект и очистили список в Redis")
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
        logger.info(
            "Удалили ORM-объект из БД и запись из кэша Redis",
        )
        # print("Удалили запись из кэша редис")
    await clear_cache()
    logger.info(
        "Очищаем key-value для списка в Redis, тк после изменения он мог устареть",
    )
    # print("Обновили объект и очистили список в Redis")
    return singer


async def clear_cache():
    keys = await redis.keys("singers:*")
    if keys:
        await redis.delete(*keys)
        # logger.info("Получили все ключи для списка и удалили их из Redis")
        # print("Очистили список singers в Redis")
