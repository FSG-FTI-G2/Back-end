import time
from typing import Optional, Any
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    code: int = Field(None, alias="code")
    message: str = Field(None, alias="message")
    data: Optional[Any] = Field(None, alias="data")
    errors: Optional[Any] = Field(None, alias="errors")
    timestamp: int = Field(None, alias="timestamp")

def response(code: int, message: str, data: Optional[Any] = None, errors: Optional[Any] = None) -> dict:
    return ResponseModel(
        code=code,
        message=message,
        data=data,
        errors=errors,
        timestamp=int(time.time())
    ).model_dump() 
