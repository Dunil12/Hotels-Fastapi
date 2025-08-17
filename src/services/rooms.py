from datetime import date

from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException
from src.schemas.facility import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):

    async def get_rooms_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        hotel = await HotelService(self.db).get_hotel_by_id(hotel_id=hotel_id)
        await self.db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


    async def get_room_by_id(
            self,
            room_id: int,
    ):
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException


    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest,
    ):
        hotel = await HotelService(self.db).get_hotel_by_id(hotel_id=hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [RoomFacilityAdd(facility_id=facility_id, room_id=room.id)
                                 for facility_id in room_data.facilities_ids_to_add]
        await self.db.rooms_facilities.add_batch(rooms_facilities_data)
        await self.db.commit()

        return room


    async def delete_room(
            self,
            room_id: int,
            hotel_id: int,
    ):
        hotel = await HotelService(self.db).get_hotel_by_id(hotel_id=hotel_id)

        try:
            room = await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
        await self.db.commit()
        return room


    async def change_room(
            self,
            new_room_data: RoomAddRequest,
            hotel_id: int,
            room_id: int,
    ):
        hotel = await HotelService(self.db).get_hotel_by_id(hotel_id=hotel_id)

        _new_room_data = RoomAdd(hotel_id=hotel_id, **new_room_data.model_dump())

        try:
            await self.db.rooms.change(_new_room_data, id=room_id)
        except NoResultFound:
            raise RoomNotFoundException

        if new_room_data.facilities_ids_to_remove:
            await self.db.rooms_facilities.delete_batch(room_id=room_id,
                                                   facilities_ids=new_room_data.facilities_ids_to_remove)
        if new_room_data.facilities_ids_to_add:
            rooms_facilities_data_to_add = [RoomFacilityAdd(facility_id=facility_id, room_id=room_id)
                                            for facility_id in new_room_data.facilities_ids_to_add]
            await self.db.rooms_facilities.add_batch(rooms_facilities_data_to_add)

        await self.db.commit()