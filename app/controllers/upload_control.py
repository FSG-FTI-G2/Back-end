import os
import shutil
from fastapi import UploadFile, HTTPException
import asyncio

UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "../upload_files")
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg"}
MAX_FILE_SIZE_MB = 20

def validate_file_size(file: UploadFile, max_size_mb: int = MAX_FILE_SIZE_MB):
    file_size = len(file.file.read())
    if file_size > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size exceeds {max_size_mb} MB limit")

def validate_file_extension(file: UploadFile):
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File extension not allowed")

async def save_uploaded_file(file: UploadFile):
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File extension not allowed")

    file_size = len(file.file.read())
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 20MB size limit")
    
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": "File uploaded successfully"}

async def upload_progress(websocket):
    await websocket.accept()
    progress = 0

    # Simulate file upload progress and notify the client
    while progress < 100:
        await websocket.send_text(f"Upload progress: {progress}%")
        progress += 10
        await asyncio.sleep(0.5)

    await websocket.send_text("Upload completed")
    await websocket.close()
