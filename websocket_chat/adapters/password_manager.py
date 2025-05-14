from passlib.context import CryptContext

from websocket_chat.domain.interfaces.password_manager import IPasswordManager


class PasswordManager(IPasswordManager):
    def __init__(self) -> None:
        self._context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__default_rounds=12,
        )

    def hash_password(self, *, password: str) -> str:
        return self._context.hash(password)

    def verify_password(self, *, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)
