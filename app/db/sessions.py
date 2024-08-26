from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings
from db.base import Base

# Создаю движок для подключения к базе данных
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# SessionLocal — это фабрика сессий.
# Сессия — это "обертка" над соединением с базой данных,
# которая позволяет выполнять запросы к базе.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
