from sqlalchemy.future import select
from db.sessions import AsyncSession
from applications.users.models import User


async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()