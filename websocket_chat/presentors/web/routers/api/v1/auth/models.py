from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRegisterModel(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    device_id: UUID


class TokenPairModel(BaseModel):
    access_token: str
    refresh_token: str


class LoginUserModel(BaseModel):
    email: EmailStr
    password: str
    device_id: UUID


class RefreshInModel(BaseModel):
    refresh_token: str
