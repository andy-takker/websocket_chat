from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, PositiveInt

from websocket_chat.application.errors import WebsockerChatException


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
        message=exc.message,
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
