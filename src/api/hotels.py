from fastapi import Query, APIRouter
from sqlalchemy import insert, select
from first_project.src.api.dependencies import PaginationDep
from first_project.src.database import async_session_maker
from first_project.src.models.hotels import HotelsOrm
from first_project.src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
def func():
    return "HelloWorld!!!"

@router.get("",
            summary="Получение отелей по фильтрам title и location",
            description="<h1>Документация к ручке get_hotel</h1>",)
async def get_hotel(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположение"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = (query
                     .filter(HotelsOrm
                     .title.contains(title)))
        if location:
            query = (query
                     .filter(HotelsOrm
                     .location.contains(location)))

        query = (query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels



@router.post("")
async def create_hotel(
        hotel_data: Hotel
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(table=HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
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
