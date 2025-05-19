import pytest

from websocket_chat.adapters.password_manager import PasswordManager


@pytest.fixture
def password_manager() -> PasswordManager:
    return PasswordManager()
