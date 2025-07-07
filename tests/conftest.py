# ruff: noqa: E402
import pytest
from httpx import ASGITransport, AsyncClient

from unittest import mock

from typing_extensions import AsyncGenerator

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from first_project.src.api.dependencies import get_db
from first_project.src.config import settings
from first_project.src.database import Base, engine_null_pool, async_session_maker_null_pool
from first_project.src.main import app
from first_project.src.models import * # noqa: F403
from first_project.src.repositories.hotels import HotelsRepository
from first_project.src.repositories.rooms import RoomsRepository
from first_project.src.utils.db_manager import DBManager
from first_project.tests.utils.parser import Parser



@pytest.fixture(autouse=True, scope="session")
def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db

@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        hotels = Parser().parse_hotels()
        rooms = Parser().parse_rooms()

        await HotelsRepository(conn).add_batch(hotels)
        await RoomsRepository(conn).add_batch(rooms)

@pytest.fixture(autouse=True, scope="session")
async def fill_database(setup_database):
    hotels = Parser().parse_hotels()
    rooms = Parser().parse_rooms()

    async with engine_null_pool.begin() as conn:
        await HotelsRepository(conn).add_batch(hotels)
        await RoomsRepository(conn).add_batch(rooms)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True, scope="session")
async def register_user(ac, setup_database):
    await ac.post("/auth/register",
                  json={
                      "email":"email@gmail.com",
                      "password": "password"
                  })


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    response = await ac.post("/auth/login",
                      json={
            "email": "email@gmail.com",
            "password": "password"},)

    assert response.status_code == 200
    assert ac.cookies["access_token"]

    yield ac


