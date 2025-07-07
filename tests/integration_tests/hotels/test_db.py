from first_project.src.schemas.hotels import HotelAdd

async def test_create_hotel(db):
    hotel_data = HotelAdd(title="title", location="location")

    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    assert new_hotel
