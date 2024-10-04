from fastapi import APIRouter, UploadFile, File, WebSocket
from fastapi.responses import JSONResponse
from app.controllers.upload_control import save_uploaded_file, upload_progress

router = APIRouter()

# File upload endpoint
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    response = await save_uploaded_file(file)
    return JSONResponse(content=response)

# WebSocket connection to monitor upload progress
@router.websocket("/ws/progress/")
async def websocket_endpoint(websocket: WebSocket):
    await upload_progress(websocket)
