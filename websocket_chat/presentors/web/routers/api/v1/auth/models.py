from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterModel(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    device_id: UUID


class TokenPairModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str


class LoginUserModel(BaseModel):
    email: EmailStr
    password: str
    device_id: UUID = Field(default_factory=uuid4)


class RefreshInModel(BaseModel):
    refresh_token: str
