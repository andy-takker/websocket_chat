from enum import StrEnum

from pydantic import BaseModel


class StatusType(StrEnum):
    OK = "ok"
    ERROR = "error"


class StatusModel(BaseModel):
    status: StatusType
