from models.singer import SingerOrm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.singer import CreateSinger, UpdateSinger
from sqlalchemy import select
from fastapi import HTTPException, status


async def create_singer_crud(singer_in: CreateSinger, session: AsyncSession):
    new_singer = SingerOrm(**singer_in.model_dump())
    session.add(new_singer)
    await session.commit()
    await session.refresh(new_singer)
    return new_singer


async def get_singer_by_id_crud(singer_id: int, session: AsyncSession):
    singer = await session.get(SingerOrm, singer_id)
    return singer


async def get_list_singer_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(SingerOrm).order_by(SingerOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_singer_partial_crud(
    singer_in: UpdateSinger, singer_id: int, session: AsyncSession
):
    update_singer = await get_singer_by_id_crud(singer_id=singer_id, session=session)
    if not update_singer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Певец не найден"
        )
    singer_data: dict = singer_in.model_dump(exclude_unset=True)
    if not singer_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    for k, v in singer_data.items():
        setattr(update_singer, k, v)
    await session.commit()
    await session.refresh(update_singer)
    return update_singer


async def delete_singer_crud(singer_id: int, session: AsyncSession):
    singer = await get_singer_by_id_crud(singer_id=singer_id, session=session)
    if not singer:
        return None
    await session.delete(singer)
    await session.commit()
    return True
