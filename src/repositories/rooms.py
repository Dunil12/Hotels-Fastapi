
from first_project.src.models.rooms import RoomsOrm
from first_project.src.repositories.base import BaseRepository
from first_project.src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

