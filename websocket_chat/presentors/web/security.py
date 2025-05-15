from typing import Final

from fastapi.security import OAuth2PasswordBearer

OAUTH2_SCHEME: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)
