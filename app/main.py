from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import tasks, users
from app.db.database import create_db_and_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_session
    yield

app = FastAPI(title="Simple Task Manager API",
              description="An API to manage your tasks efficiently.",
              lifespan=lifespan)

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(users.router, prefix="/users", tags=["Users"])