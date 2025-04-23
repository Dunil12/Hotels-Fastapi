from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from first_project.src.api.hotels import router as router_hotels



app = FastAPI()

app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.8", port=8000, reload=True)