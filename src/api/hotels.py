from datetime import date

from fastapi import Query, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import CheckinDateLaterThanCheckoutDateException, ObjectNotFoundException, \
    HotelNotFoundHTTPException, CheckinDateLaterThanCheckoutDateHTTPException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("",
            summary="Получение отелейй по фильтрам title и location",
            description="<h1>Документация к ручке get_all_hotels</h1>",)
async def get_all_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположение"),
    date_from: date = Query(example="2025-05-10"),
    date_to: date = Query(example="2025-05-11"),
):
    try:
        hotels = await HotelService(db).get_hotels(
            pagination=pagination,
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
        )
    except CheckinDateLaterThanCheckoutDateException:
        raise CheckinDateLaterThanCheckoutDateHTTPException
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": hotels}

@router.get("/{hotel_id}", summary="Получение отеля по id",)
async def get_hotel(
        db: DBDep,
        hotel_id: int,
):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd
):
    hotel = await HotelService(db).create_hotel(hotel_data=hotel_data)

    return {"status": "OK", "data": hotel}


# @router.post("")
# async def create_hotels(
#     db: DBDep,
#     hotel_data: list[HotelAdd]
# ):
#     hotel = await db.hotels.add_batch(hotel_data)
#     await db.commit()
#
#     return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    try:
        await HotelService(db).delete_hotel(
            hotel_id=hotel_id,
            title=title,
            location=location
        )
    except HotelNotFoundHTTPException:
        raise HotelNotFoundHTTPException


@router.patch("/{hotel_id}")
async def change_hotel(
    db: DBDep,
    new_hotel_data: HotelPatch,
    hotel_id: int,
    title: str | None = Query(None),
    location: str | None = Query(None),
):
    try:
        await HotelService(db).change_hotel(
            new_hotel_data=new_hotel_data,
            hotel_id=hotel_id,
            title=title,
            location=location,
        )
    except HotelNotFoundHTTPException:
        raise HotelNotFoundHTTPException