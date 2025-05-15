from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, PositiveInt

from websocket_chat.application.errors import (
    IncorrectCredentialsException,
    ObjectNotFoundException,
    UserAlreadyExistsException,
    WebsockerChatException,
)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _exception_json_response(
        status_code=exc.status_code,
        message=exc.detail,
    )


async def websocket_chat_exception_handler(
    request: Request,
    exc: WebsockerChatException,
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=str(exc),
    )


async def user_already_exists_exception_handler(
    request: Request,
    exc: UserAlreadyExistsException,
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.CONFLICT,
        message=str(exc),
    )


async def object_not_found_exception_handler(
    request: Request,
    exc: ObjectNotFoundException,
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.NOT_FOUND,
        message=str(exc),
    )


async def credentials_exception_handler(
    request: Request,
    exc: IncorrectCredentialsException,
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.UNAUTHORIZED,
        message=str(exc),
    )


def _exception_json_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=StatusResponseModel(
            ok=False,
            status_code=status_code,
            message=message,
        ).model_dump(mode="json"),
    )


class StatusResponseModel(BaseModel):
    ok: bool
    status_code: PositiveInt
    message: str
