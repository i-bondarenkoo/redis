from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from db.database import get_session
from schemas.singer import CreateSinger, ResponseSinger, UpdateSinger
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import crud
from services.redis_service import (
    create_singer_and_cache,
    get_singer_by_id_and_cache,
    update_singer_and_cache,
    delete_singer_and_cache,
    get_list_singers_and_cache,
)

router = APIRouter(
    prefix="/singers",
    tags=["Singers"],
)


@router.post("/", response_model=ResponseSinger)
async def create_singer(
    singer_in: Annotated[
        CreateSinger, Body(description="Поля для создания модели певца")
    ],
    session: AsyncSession = Depends(get_session),
):
    return await create_singer_and_cache(singer_in=singer_in, session=session)


@router.get("/{singer_id}", response_model=ResponseSinger)
async def get_singer_by_id(
    singer_id: Annotated[
        int, Path(gt=0, description="ID певца для поиска подробной информации")
    ],
    session: AsyncSession = Depends(get_session),
):
    singer = await get_singer_by_id_and_cache(singer_id=singer_id, session=session)
    if not singer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Певец не найден"
        )
    return singer


@router.get("/", response_model=list[ResponseSinger])
async def get_list_singers(
    start: int = Query(0, description="Начальный индекс списка"),
    stop: int = Query(3, description="Конечный индекс списка"),
    session: AsyncSession = Depends(get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Начальный индекс списка не может быть больше конечного",
        )
    return await get_list_singers_and_cache(start=start, stop=stop, session=session)


@router.patch("/{singer_id}", response_model=ResponseSinger)
async def update_singer_patch(
    singer_in: Annotated[
        UpdateSinger, Body(description="Поля для обновления записи в БД")
    ],
    singer_id: Annotated[int, Path(gt=0, description="ID Певца для обновления")],
    session: AsyncSession = Depends(get_session),
):
    return await update_singer_and_cache(
        singer_in=singer_in, singer_id=singer_id, session=session
    )


@router.delete("/{singer_id}")
async def delete_singer(
    singer_id: Annotated[int, Path(gt=0, description="ID Певца для удаления")],
    session: AsyncSession = Depends(get_session),
):
    singer = await delete_singer_and_cache(singer_id=singer_id, session=session)
    return {"message": "певец удален"}
