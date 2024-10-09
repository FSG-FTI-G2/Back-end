from typing import List, Optional
from fastapi import HTTPException
from app.utils.response import paginated_response, PaginatedResponseModel
from app.configs.mongodb import db
from pymongo import DESCENDING
from app.models.user import UserSchema
from bson import ObjectId


def convert_objectid_to_str(document):
    if "_id" in document and isinstance(document["_id"], ObjectId):
        document["_id"] = str(document["_id"])
    return document


# Function to query files
async def get_files_control(
    page_size: int = 10, 
    page_index: int = 1, 
    search: Optional[str] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    user: UserSchema = None
) -> PaginatedResponseModel:
    # Validate pagination parameters
    if page_size <= 0 or page_index <= 0:
        raise HTTPException(status_code=400, detail="Page size and index must be positive integers.")
    
    # Build query filter
    query = {}

    # Add user_id filter if provided (ensure user_id is treated as a string)
    if user:
        query["user_id"] = user.id  

    # Add file_name search filter if provided
    if search:
        query["file_name"] = {"$regex": search, "$options": "i"}  

    # Add file_type filter if provided and ensure the value is properly validated
    if file_type:
        file_type_lower = file_type.lower()
        if file_type_lower in ["pdf", "docx", "txt", "png", "jpeg"]:
            query["type"] = file_type_lower  # Ensure exact match of file_type
        else:
            raise HTTPException(status_code=400, detail="Invalid file_type provided.")
    
    # Add status filter if provided and ensure the value is properly validated
    if status:
        status_lower = status.lower()
        if status_lower in ["pending", "uploading", "processing", "success", "error"]:
            query["status"] = status_lower  # Ensure exact match of status
        else:
            raise HTTPException(status_code=400, detail="Invalid status provided.")
    
    # Get total count of files matching the query
    total_files = db["files"].count_documents(query)
    
    # Calculate pagination
    skip = (page_index - 1) * page_size
    
    # Fetch files from database
    cursor = db["files"].find(query).skip(skip).limit(page_size).sort("created_at", DESCENDING)
    files = cursor.to_list(length=page_size)
    files = [convert_objectid_to_str(file) for file in files]
    
    # Return paginated results
    return paginated_response(files, total_files, page_index, page_size)
