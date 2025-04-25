from first_project.src.models.rooms import RoomsOrm
from first_project.src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm

