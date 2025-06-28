from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from first_project.src.init import redis_manager
from first_project.src.api.hotels import router as router_hotels
from first_project.src.api.auth import router as router_auth
from first_project.src.api.rooms import router as router_rooms
from first_project.src.api.bookings import router as router_bookings
from first_project.src.api.facilities import router as router_facilities


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # при выключении/перезагрузке приложения

    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.21", port=8000, reload=True)