from datetime import date

from fastapi import Query, APIRouter

from first_project.src.api.dependencies import PaginationDep, DBDep
from first_project.src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("",
            summary="Получение отелейй по фильтрам title и location",
            description="<h1>Документация к ручке get_hotel</h1>",)
async def get_all_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположение"),
    date_from: date = Query(example="2025-05-10"),
    date_to: date = Query(example="2025-05-11"),
):
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)

    print("limit=", limit)
    print("offset=", offset)

    return await db.hotels.get_filtered_by_date(
        title=title,
        location=location,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
    )

@router.get("/{hotel_id}", summary="Получение отеля по id",)
async def get_hotel(
        db: DBDep,
        hotel_id: int,
):
    return await db.hotels.get_one_or_none(**{"id" : hotel_id})


# @router.post("")
# async def create_hotel(
#     db: DBDep,
#     hotel_data: HotelAdd
# ):
#     hotel = await db.hotels.add(hotel_data)
#     await db.commit()
#     print(hotel)
#
#     return {"status": "OK"}

@router.post("")
async def create_hotels(
    db: DBDep,
    hotel_data: list[HotelAdd]
):
    print("hotel_data = ", hotel_data)
    hotel = await db.hotels.add_batch(hotel_data)
    await db.commit()
    print(hotel)

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    await db.hotels.delete(id=hotel_id, title=title, location=location)
    await db.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}")
async def change_hotel(
    db: DBDep,
    new_hotel_data: HotelPatch,
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    if hotel_id or title or location:
        hotel = await db.hotels.change(new_hotel_data, id=hotel_id, title=title, location=location)
        await db.commit()
        print(hotel)
        return hotel
    else:
        return {"status" : "Fill one or more required fields"}