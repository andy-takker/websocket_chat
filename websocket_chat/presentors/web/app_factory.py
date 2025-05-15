import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Final

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, HTTPException

from websocket_chat.adapters.di import AdaptersProvider
from websocket_chat.application.errors import (
    IncorrectCredentialsException,
    ObjectNotFoundException,
    UserAlreadyExistsException,
    WebsockerChatException,
)
from websocket_chat.application.logging import setup_logging
from websocket_chat.domain.di import DomainProvider
from websocket_chat.presentors.web.config import Config
from websocket_chat.presentors.web.exception_handlers import (
    credentials_exception_handler,
    http_exception_handler,
    object_not_found_exception_handler,
    user_already_exists_exception_handler,
    websocket_chat_exception_handler,
)
from websocket_chat.presentors.web.routers.api.router import router as api_router

log = logging.getLogger(__name__)

ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]

EXCEPTION_HANDLERS: Final[ExceptionHandlersType] = (
    (HTTPException, http_exception_handler),
    (Exception, websocket_chat_exception_handler),
    (WebsockerChatException, websocket_chat_exception_handler),
    (ObjectNotFoundException, object_not_found_exception_handler),
    (UserAlreadyExistsException, user_already_exists_exception_handler),
    (IncorrectCredentialsException, credentials_exception_handler),
)


def get_application() -> FastAPI:
    config = Config()
    return WebService(config=config).create_application()


@dataclass(frozen=True, kw_only=True, slots=True)
class WebService:
    config: Config

    def create_application(self) -> FastAPI:
        setup_logging(
            log_level=self.config.log.log_level, use_json=self.config.log.use_json
        )

        app = FastAPI(
            debug=self.config.app.debug,
            title=self.config.app.title,
            description=self.config.app.description,
            version=self.config.app.version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
            lifespan=_lifespan,
        )

        self._set_middlewares(app=app)
        self._set_routes(app=app)
        self._set_exception_handlers(app=app)
        self._set_dependencies(app=app)

        log.info("Application configured")
        return app

    def _set_middlewares(self, app: FastAPI) -> None:
        pass

    def _set_routes(self, app: FastAPI) -> None:
        app.include_router(api_router)

    def _set_exception_handlers(self, app: FastAPI) -> None:
        for exception, handler in EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def _set_dependencies(self, app: FastAPI) -> None:
        container = make_async_container(
            AdaptersProvider(
                database_config=self.config.db,
                jwt_config=self.config.jwt,
                debug=self.config.app.debug,
                redis_config=self.config.redis,
            ),
            DomainProvider(),
        )
        setup_dishka(container=container, app=app)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()
