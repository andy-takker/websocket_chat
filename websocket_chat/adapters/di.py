from dishka import BaseScope, Component, Provider, Scope, provide

from websocket_chat.adapters.database.config import DatabaseConfig
from websocket_chat.adapters.password_manager import PasswordManager
from websocket_chat.domain.interfaces.password_manager import IPasswordManager


class AdaptersProvider(Provider):
    def __init__(
        self,
        database_config: DatabaseConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ):
        super().__init__(scope, component)
        self._database_config = database_config

    @provide(scope=Scope.APP)
    def password_manager(self) -> IPasswordManager:
        return PasswordManager()
