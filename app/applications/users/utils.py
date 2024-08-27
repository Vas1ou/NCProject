from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from db.sessions import get_db
from .crud import get_user
from utils.hash import verify_password
from .application_settings import SECRET_KEY, ALGORITHM, oauth2_scheme
from .schemas import TokenData


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        # Извлекаем время истечения срока действия токена
        exp_timestamp = payload.get("exp")

        # Конвертируем время в формат datetime
        exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        # Вычисляем текущее время
        current_time = datetime.now(timezone.utc)

        # Остаточное время жизни токена
        time_remaining = exp_time - current_time
        print(f'ОСТАТОЧНОЕ ВРЕМЯ ЖИЗНИ ТОКЕНА {time_remaining}')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user

