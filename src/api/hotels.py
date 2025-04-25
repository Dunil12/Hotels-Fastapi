from fastapi import Query, APIRouter
from sqlalchemy import insert, select
from first_project.src.api.dependencies import PaginationDep
from first_project.src.database import async_session_maker
from first_project.src.models.hotels import HotelsOrm
from first_project.src.repositories.hotels import HotelsRepository
from first_project.src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
def func():
    return "HelloWorld!!!"

@router.get("",
            summary="Получение отелейй по фильтрам title и location",
            description="<h1>Документация к ручке get_hotel</h1>",)
async def get_hotel(
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


@router.post("")
async def create_hotel(
        hotel_data: Hotel
):
    async with (async_session_maker() as session):
        # new_hotel =
        await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK"}

@router.patch("/{hotel_id}")
def change_data(
    hotel_id : int,
    hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["location"] = hotel_data.location
            return {"status": "ok"}
    return {"status": "none"}
