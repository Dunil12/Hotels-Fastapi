from sqlalchemy import delete

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facility import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def delete_batch(self, room_id: int, facilities_ids: list[int]):
        delete_data_stmt = (
            delete(table=self.model)
            .filter(RoomsFacilitiesOrm.facility_id.in_(facilities_ids))
            .filter_by(room_id=room_id)
        )
        print(delete_data_stmt.compile(compile_kwargs={"literal_binds": True}))

        await self.session.execute(delete_data_stmt)
        return {"status": "200"}
