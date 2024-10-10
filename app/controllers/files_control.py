from typing import Optional
from fastapi import HTTPException
from app.models.file import FileSchema, FileType, FileStatus
from app.models.user import UserSchema


# Function to query files
async def get_files_control(
    user: UserSchema,
    page_size: int = 10,
    page_index: int = 0,
    search: Optional[str] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
):
    # Validate pagination parameters
    if page_size < 0 or page_index < 0:
        raise HTTPException(
            status_code=400, detail="Page size and index must be positive integers.")

    # Build query filter
    query = {}

    # Add file_name search filter if provided
    if search:
        query["file_name"] = {"$regex": search, "$options": "i"}

    # Add file_type filter if provided and ensure the value is properly validated
    if file_type:
        if file_type.upper() in FileType.__members__:
            # Ensure exact match of file_type
            query["type"] = file_type.lower()
        else:
            raise HTTPException(
                status_code=400, detail="Invalid file_type provided.")

    # Add status filter if provided and ensure the value is properly validated
    if status:
        if status.upper() in FileStatus.__members__:
            query["status"] = file_type.lower()  # Ensure exact match of status
        else:
            raise HTTPException(
                status_code=400, detail="Invalid status provided.")

    # Query database for files
    files = FileSchema.find_by_user_id(
        user.id, page_size, page_index, query=query)
    total_pages = FileSchema.page_count(page_size)

    # Return paginated results
    return files, total_pages
