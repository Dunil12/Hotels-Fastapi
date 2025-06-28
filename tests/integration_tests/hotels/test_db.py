from first_project.src.database import async_session_maker, async_session_maker_null_pool
from first_project.src.schemas.hotels import HotelAdd
from first_project.src.utils.db_manager import DBManager


async def test_create_hotel():
    hotel_data = HotelAdd(title="title", location="location")

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
    print(f"{new_hotel=}")
    print("!!!")
    assert new_hotel
