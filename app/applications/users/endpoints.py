from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserBase
from .models import User
from db.sessions import get_db

router = APIRouter()


@router.post('/user/', response_model=UserBase)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user