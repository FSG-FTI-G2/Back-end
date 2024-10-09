import time
from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field
from fastapi.responses import ORJSONResponse


class PaginatedResponseModel(BaseModel):
    files: List[Any]  # Sửa lại tên trường cho nhất quán
    total_files: int
    page_index: int
    page_size: int


class ResponseModel(BaseModel):
    code: int = Field(None, alias="code")
    message: str = Field(None, alias="message")
    data: Optional[Any] = Field(None, alias="data")
    errors: Optional[Any] = Field(None, alias="errors")
    timestamp: int = Field(None, alias="timestamp")


def response(code: int, message: str, data: Optional[Any] = None, error: Optional[Any] = None) -> dict:
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


def paginated_response(files: List[Any], total_files: int, page_index: int, page_size: int) -> Dict[str, Any]:
    return {
        "files": files,
        "total_files": total_files,
        "page_index": page_index,
        "page_size": page_size
    }
