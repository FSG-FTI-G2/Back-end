from typing import Annotated
import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from app.middlewares.middleware import auth_user_middleware
from app.controllers.upload_controller import upload_files_controller, upload_file_status_controller
from app.providers import state
from app.models.user import UserSchema
from app.utils.response import response

router = APIRouter()


@router.post("/")
async def upload_file(
    files: Annotated[list[UploadFile], File(...)],
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
    background_tasks: BackgroundTasks
):
    # Read file data
    files_name = [file.filename for file in files]
    files_byte = [await file.read() for file in files]
    files_data = list(zip(files_name, files_byte))
    # Initialize file state for tracking upload status
    state.set(user.id, {})
    # Upload files in background
    background_tasks.add_task(upload_files_controller, files_data, user)
    return response(code=200, message="Files are being uploaded.")


@router.websocket("/ws")
async def upload_file_progress(
    websocket: WebSocket,
    user: Annotated[UserSchema, Depends(auth_user_middleware)]
):
    await websocket.accept()
    try:
        is_completed = False
        while not is_completed:
            await asyncio.sleep(1)
            is_completed, status = upload_file_status_controller(user.id)
            await websocket.send_json(response(status_code=200, message="File upload status.", data={
                "status": status,
                "is_completed": is_completed
            }))
    except WebSocketDisconnect:
        # Remove user state on disconnect
        state.remove(user.id)
        await websocket.close()
