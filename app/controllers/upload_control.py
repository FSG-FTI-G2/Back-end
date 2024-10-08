import os
from fastapi import UploadFile, HTTPException, WebSocket
from typing import List
from app.models.file import FileSchema, FileType, FileStatus
from app.providers import file_db
import shutil
import magic  # To detect file MIME type
from pymongo.errors import PyMongoError
from minio import Minio
from minio.error import S3Error

# Define the allowed file extensions and max file size (20MB)
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx", "png", "jpeg"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

minio_client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="rxdR6Lna48CnzV5NHdtV",
    secret_key="bofSGRbwkVzSVly46sGz791suiEFZEH6h9HNdaWF",
    secure=False  
)

def validate_file_extension(file: UploadFile) -> bool:
    """
    Validate if the file extension is allowed.
    """
    file_extension = file.filename.split(".")[-1].lower()
    return file_extension in ALLOWED_EXTENSIONS

def validate_file_size(file: UploadFile) -> bool:
    """
    Validate if the file size is within the limit.
    """
    if file.file.seek(0, os.SEEK_END) > MAX_FILE_SIZE:
        return False
    file.file.seek(0)  # Reset the file pointer after checking size
    return True

async def upload_file_to_minio(file: UploadFile, bucket_name: str, object_name: str):
    try:
        # Tạo bucket nếu chưa tồn tại
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        
        # Tải file lên
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file.file,  # Lưu ý: `file.file` là file-like object
            length=file.size,  # Kích thước của file
            content_type=file.content_type  # Loại nội dung
        )
        return f"File {object_name} uploaded to MinIO successfully."
    except S3Error as e:
        print(f"Error occurred: {e}")
        return None
    

async def save_file(file: UploadFile, user_id: str) -> FileSchema:
    """
    Save the uploaded file and file metadata into MongoDB.
    """
    if not validate_file_extension(file):
        raise HTTPException(status_code=400, detail="Invalid file extension.")
    
    if not validate_file_size(file):
        raise HTTPException(status_code=400, detail="File exceeds the size limit of 20MB.")
    
    try:
        # Create a directory to save the file
        upload_dir = f"./uploads/{user_id}/"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)

        # Save the file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file type (using MIME detection)
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        
        # Map MIME type to FileType Enum
        if mime_type.startswith("application/pdf"):
            file_type = FileType.PDF
        elif mime_type.startswith("text/"):
            file_type = FileType.TXT
        elif mime_type.startswith("application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            file_type = FileType.DOCX
        elif mime_type.startswith("image/png"):
            file_type = FileType.PNG
        elif mime_type.startswith("image/jpeg"):
            file_type = FileType.JPEG
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        
        # Save file metadata in MongoDB
        file_schema = FileSchema(
            user_id=user_id,
            type=file_type,
            file_name=file.filename,
            file_path=file_path,
            status=FileStatus.PENDING
        )
        file_schema.create()  # Save metadata to MongoDB
        
        return file_schema
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

async def upload_file_with_progress(file: UploadFile, user_id: str, websocket: WebSocket):
    """
    Function to upload a file and send upload progress via WebSocket.
    """
    try:
        await websocket.accept()

        # Notify WebSocket connection about file upload start
        await websocket.send_text(f"Starting upload for file: {file.filename}")
        
        # Initialize file upload status in MongoDB
        file_schema = FileSchema(
            user_id=user_id,
            type=FileType.PENDING,  # Initial type will be updated later
            file_name=file.filename,
            file_path="",
            status=FileStatus.UPLOADING
        )
        file_schema.create()

        # Create a directory to save the file
        upload_dir = f"./uploads/{user_id}/"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)

        # Upload the file in chunks to simulate progress
        total_size = 0
        chunk_size = 1024 * 1024  # 1MB per chunk
        with open(file_path, "wb") as buffer:
            while chunk := file.file.read(chunk_size):
                total_size += len(chunk)
                buffer.write(chunk)
                
                # Calculate progress and send it via WebSocket
                progress = (total_size / file.file._file.seek(0, os.SEEK_END)) * 100
                await websocket.send_text(f"Upload progress: {progress:.2f}%")
                file.file.seek(total_size)  # Move pointer to the correct place

        # Update file status and metadata in MongoDB after upload
        file_schema.file_path = file_path
        file_schema.type = validate_file_extension(file)  # Update file type
        file_schema.status = FileStatus.SUCCESS
        file_schema.update()

        await websocket.send_text(f"File {file.filename} uploaded successfully.")
        await websocket.close()

    except Exception as e:
        file_schema.status = FileStatus.ERROR
        file_schema.update()
        await websocket.send_text(f"Error during upload: {str(e)}")
        await websocket.close()
