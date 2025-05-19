import pytest

from websocket_chat.adapters.password_manager import PasswordManager


@pytest.mark.parametrize("password", ["random", "password", "123489*(&^#$)  "])
def test_hash_and_verify_password(
    password: str,
    password_manager: PasswordManager,
) -> None:
    hashed_password = password_manager.hash_password(password=password)
    assert password_manager.verify_password(
        plain_password=password, hashed_password=hashed_password
    )
