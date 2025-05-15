from http import HTTPStatus

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from websocket_chat.domain.entities.token import RefreshIn
from websocket_chat.domain.entities.user import LoginUser, UserRegister
from websocket_chat.domain.use_cases.login_user import LoginUserUseCase
from websocket_chat.domain.use_cases.refesh_token import RefreshTokenUseCase
from websocket_chat.domain.use_cases.register_user import (
    RegisterUserUseCase,
)
from websocket_chat.presentors.web.routers.api.v1.auth.models import (
    LoginUserModel,
    RefreshInModel,
    TokenPairModel,
    UserRegisterModel,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    response_model=TokenPairModel,
    status_code=HTTPStatus.CREATED,
)
async def register(
    register_user: FromDishka[RegisterUserUseCase],
    payload: UserRegisterModel,
) -> TokenPairModel:
    token_pair = await register_user.execute(
        input_dto=UserRegister(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            device_id=payload.device_id,
        ),
    )
    return TokenPairModel.model_validate(token_pair)


@router.post(
    "/login",
    response_model=TokenPairModel,
    status_code=HTTPStatus.OK,
)
async def login(
    payload: LoginUserModel,
    login_user: FromDishka[LoginUserUseCase],
) -> TokenPairModel:
    token_pair = await login_user.execute(
        input_dto=LoginUser(
            email=payload.email,
            password=payload.password,
            device_id=payload.device_id,
        ),
    )
    return TokenPairModel.model_validate(token_pair)


@router.post(
    "/refresh",
    response_model=TokenPairModel,
    status_code=HTTPStatus.OK,
)
async def refresh_tokens(
    payload: RefreshInModel,
    refresh_token: FromDishka[RefreshTokenUseCase],
) -> TokenPairModel:
    token_pair = await refresh_token.execute(
        input_dto=RefreshIn(
            refresh_token=payload.refresh_token,
        ),
    )
    return TokenPairModel.model_validate(token_pair)
