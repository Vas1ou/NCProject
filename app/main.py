from fastapi import FastAPI
from core.config import settings
from applications.users.endpoints import router as users_routers
from db.sessions import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
# Подключение маршрутов
app.include_router(users_routers, prefix='/users', tags=['users'])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
