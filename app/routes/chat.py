from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserSchema
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.chat_controller import get_all_history, get_messages_by_id, add_message, delete_message
from app.utils.prompt_template import RolePrompt
from app.utils.response import response


router = APIRouter()


@router.get("/")
async def get_all_chat_hostory(
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
):
    histories = await get_all_history(user)
    return response(200, "Success", data=[history.model_dump() for history in histories])


class MessageInput(BaseModel):
    message: str
    message_id: Optional[str] = None
    role: Optional[RolePrompt] = RolePrompt.GENERAL


@router.post("/")
async def add_new_messages(
    data: MessageInput,
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
):
    # Lưu hoặc cập nhật tin nhắn
    message = await add_message(message=data.message, message_id=data.message_id, role=data.role, user=user)
    return response(200, "Success", data=message.model_dump())


@router.get("/{message_id}")
async def get_all_messages(message_id: str, user: Annotated[UserSchema, Depends(auth_user_middleware)]):
    messages = await get_messages_by_id(message_id, user)
    return response(200, "Success", data=[msg.model_dump() for msg in messages])


@router.delete("/{message_id}")
async def delete_user_message(
    message_id: str,
    user: UserSchema = Depends(auth_user_middleware)
):
    if await delete_message(message_id, user):
        return response(200, "Success")
    raise HTTPException(status_code=400, detail="Delete message failed")
