# ./src/agent/webapp.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.agent.routers.health_check_router import router as health_check_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_check_router)

# ... can add custom routes if needed.