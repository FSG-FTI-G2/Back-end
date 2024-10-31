from typing import Optional
import os
from fastapi import HTTPException
from app.models.file_schema import FileSchema
from app.models.user_schema import UserSchema
from app.providers import file_storage, vector_db
from app.utils.utilities import is_temp_file_exists, save_temp_file


# Function to query files
async def get_files_control(
    user: UserSchema,
    page_size: int = 10,
    page_index: int = 0,
    search: Optional[str] = None,
    type: Optional[list[str]] = None,
    status: Optional[list[str]] = None,
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
    if type:
        query["type"] = {"$in": [t.lower() for t in type]}

    # Add status filter if provided and ensure the value is properly validated
    if status:
        query["status"] = {"$in": [stat.lower() for stat in status]}

    # Query database for files
    files = FileSchema.find_by_user_id(
        user.id, page_size, page_index, query=query)
    total_pages = FileSchema.page_count(page_size)

    # Return paginated results
    return files, total_pages


async def delete_file_control(id: str, user: UserSchema):
    # Find file by id
    file = FileSchema.find_by_id(id)
    if not file:
        raise HTTPException(
            status_code=400,
            detail="File not found"
        )
    # Delete file in database
    file.delete()
    # Delete in storage
    file_storage.delete_file(file.file_path)
    # Delete vector in vector database
    vector_db.delete_vectors_by_filter(user.id, "id", file.id)


def retrieve_file(file_id_or_name: str, user: UserSchema):
    """
    Check if the file exists in the temp directory. If not, download it from MinIO.
    """
    file = FileSchema.find_by_id(file_id_or_name)
    if not file:
        # In case file_id_or_name is not an id, try to find by file name
        file = FileSchema.find_by_file_name(user.id, file_id_or_name)
        if not file:
            raise HTTPException(
                status_code=404, detail="File not found."
            )

    # Download file from storag if file does not exist in temp directory
    if not is_temp_file_exists(file.file_path):
        file_data = file_storage.download_file(file.file_path)
        # Save file to temp directory
        save_temp_file(file_data, file.file_path)

    return file
