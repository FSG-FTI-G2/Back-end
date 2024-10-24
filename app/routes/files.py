from typing import Annotated, Optional
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.upload_controller import upload_files_controller, upload_file_status_controller
from app.controllers.files_controller import get_files_control, delete_file_control, retrieve_file
from app.providers import state
from app.models.user import UserSchema
from app.utils.response import response, pagination_data

router = APIRouter()


@router.get("/")
async def get_files(
    page_size: int = 10,
    page_index: int = 0,
    search: Optional[str] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    user: UserSchema = Depends(auth_user_middleware)
):
    files, total_pages = await get_files_control(
        user=user,
        page_size=page_size,
        page_index=page_index,
        search=search,
        type=file_type.split(",") if file_type else file_type,
        status=status.split(",") if status else status
    )
    return response(code=200, message="Get files successfully.", data=pagination_data(
        data=[file.model_dump() for file in files],
        total_pages=total_pages,
        page_index=page_index,
        page_size=page_size
    ))


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
    upload_progress_id = str(uuid.uuid4())
    state.set(upload_progress_id, {})
    # Upload files in background
    background_tasks.add_task(upload_files_controller,
                              files_data, user, upload_progress_id)
    return response(code=200, message="Files are being uploaded.", data={
        "progress_id": upload_progress_id
    })


@router.websocket("/{id}")
async def upload_file_progress(websocket: WebSocket, id: str):
    await websocket.accept()
    try:
        is_completed = False
        while not is_completed:
            await asyncio.sleep(1)
            is_completed, status = await upload_file_status_controller(id)
            await websocket.send_json(response(code=200, message="File upload status.", data={
                "status": status,
                "is_completed": is_completed
            }, native=True))
    except WebSocketDisconnect:
        # Remove user state on disconnect
        state.delete(id)
        await websocket.close()


@router.delete("/{id}")
async def delete_file(
    id: str,
    user: Annotated[UserSchema, Depends(auth_user_middleware)]
):
    await delete_file_control(id, user)
    return response(code=200, message="Deleted file successfully")


@router.get("/{file_id_or_name}")
async def get_file_by_id_or_name(
    file_id_or_name: str,
    user: Annotated[UserSchema, Depends(auth_user_middleware)]
):
    file = retrieve_file(file_id_or_name, user)
    return response(code=200, message="Download file successfully.", data=file.model_dump())
