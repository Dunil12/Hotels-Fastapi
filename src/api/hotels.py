from fastapi import Query, APIRouter
from sqlalchemy import insert, select
from first_project.src.api.dependencies import PaginationDep
from first_project.src.database import async_session_maker
from first_project.src.models.hotels import HotelsOrm
from first_project.src.repositories.hotels import HotelsRepository
from first_project.src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("",
            summary="Получение отелейй по фильтрам title и location",
            description="<h1>Документация к ручке get_hotel</h1>",)
async def get_all_hotel(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположение"),
):
    async with async_session_maker() as session:
        limit = pagination.per_page or 5
        offset = limit * (pagination.page - 1)
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=limit,
            offset=offset
        )

@router.get("/{hotel_id}", summary="Получение отелейй по фильтрам title и location",)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(**{"id" : hotel_id})



@router.post("")
async def create_hotel(
    hotel_data: Hotel
):
    async with (async_session_maker() as session):
        await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK"}

@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    async with (async_session_maker() as session):
        await HotelsRepository(session).delete(id=hotel_id, title=title, location=location)
        await session.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}")
async def change_hotel(
    new_hotel_data: HotelPatch,
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    if hotel_id or title or location:
        async with (async_session_maker() as session):
            await HotelsRepository(session).change(new_hotel_data, id=hotel_id, title=title, location=location)
            await session.commit()
        return {"status" : "OK"}
    else:
        return {"status" : "Fill one or more required fields"}