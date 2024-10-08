from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect, File, HTTPException, Depends
from typing import List
from ..middlewares.middleware import auth_user_middleware
from app.controllers.upload_control import save_file, validate_file_size, upload_file_with_progress, upload_file_to_minio, validate_file_extension
from app.models.user import UserSchema  # Hàm này trả về thông tin user hiện tại

router = APIRouter()

@router.post("/")
async def upload_file(files: List[UploadFile] = File(...), current_user: UserSchema = Depends(auth_user_middleware)):
    user_id = current_user.id
    bucket_name = "admin"
    for file in files:
        # Validate file size and type
        if not validate_file_size(file):
            raise HTTPException(status_code=400, detail="File size must be less than 20MB.")
        if not validate_file_extension(file):
            raise HTTPException(status_code=400, detail="Invalid file extension.")
        
        minio_response = await upload_file_to_minio(file, bucket_name, file.filename)
        if not minio_response:
            raise HTTPException(status_code=500, detail="Failed to upload file to MinIO.")
        
        # Save file info to MongoDB with user_id
        await save_file(file, user_id)
    
    return {"message": "Files uploaded successfully."}

@router.websocket("/ws/progress/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Use WebSocket to send upload progress
        await upload_file_with_progress(websocket)
    except WebSocketDisconnect:
        print("WebSocket connection closed")
