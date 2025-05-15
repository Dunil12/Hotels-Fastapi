from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from first_project.src.api.hotels import router as router_hotels
from first_project.src.api.auth import router as router_auth
from first_project.src.api.rooms import router as router_rooms
from first_project.src.api.bookings import router as router_bookings



app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.15", port=8000, reload=True)