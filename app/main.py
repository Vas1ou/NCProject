from fastapi import FastAPI
from core.config import settings
from applications.users.endpoints import router as users_routers
from db.base import Base
from db.sessions import engine

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Подключение маршрутов
app.include_router(users_routers, prefix='/users', tags=['users'])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
