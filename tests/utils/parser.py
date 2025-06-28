import json
from pathlib import Path

from first_project.src.schemas.hotels import HotelAdd
from first_project.src.schemas.rooms import RoomAdd


class Parser:
    # schema = None
    #
    # def parse_json(self, path: str):
    #     json_data = Path(__file__).parent.parent / f"${path}"
    #
    #     with json_data.open("r", encoding="utf-8") as file:
    #         data = json.load(file)
    #
    #     return [self.schema(**item) for item in data]


    def parse_hotels(self):
        json_hotels = Path(__file__).parent.parent / "mock_hotels.json"

        with json_hotels.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [HotelAdd(**hotel) for hotel in data]

    def parse_rooms(self):
        json_rooms = Path(__file__).parent.parent / "mock_rooms.json"

        with json_rooms.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [RoomAdd(**room) for room in data]

