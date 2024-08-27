from fastapi.security import OAuth2PasswordBearer

# Конфигурация для JWT
SECRET_KEY = "nord_clan_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
