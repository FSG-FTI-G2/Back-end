from fastapi import APIRouter, Depends
from typing import List, Optional
from app.middlewares.middleware import auth_user_middleware
from app.models.user import UserSchema
from app.controllers.get_file_control import get_files_control  # Import function
from app.utils.response import PaginatedResponseModel
router = APIRouter()

# Route for querying files
@router.get("/files", response_model=PaginatedResponseModel)  # Sửa đổi để trả về PaginatedResponseModel
async def get_files(
    page_size: int = 10, 
    page_index: int = 1, 
    search: Optional[str] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    user: UserSchema = Depends(auth_user_middleware)  # Authentication middleware
):
    # Call function from controller file
    return await get_files_control(
        page_size=page_size, 
        page_index=page_index, 
        search=search, 
        file_type=file_type, 
        status=status, 
        user=user
    )
