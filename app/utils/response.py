import time
from typing import Optional, Any
from pydantic import BaseModel, Field
from fastapi.responses import ORJSONResponse


class ResponseModel(BaseModel):
    code: int = Field(None, alias="code")
    message: str = Field(None, alias="message")
    data: Optional[Any] = Field(None, alias="data")
    errors: Optional[Any] = Field(None, alias="errors")
    timestamp: int = Field(None, alias="timestamp")


def response(code: int, message: str, data: Optional[Any] = None, error: Optional[Any] = None):
    return ORJSONResponse(
        status_code=code,
        content={
            "code": code,
            "message": message,
            "data": data,
            "errors": error,
            "timestamp": int(time.time())
        }
    )
