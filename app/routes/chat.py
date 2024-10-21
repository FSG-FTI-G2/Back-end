from typing import Annotated
from fastapi import APIRouter, Depends
from app.models.user import UserSchema
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.chat_controller import get_all_history, get_messages_by_id
from app.utils.response import response, pagination_data


router = APIRouter()


@router.get("/")
async def get_all_chat_hostory(
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
):
    histories = await get_all_history(user)
    return response(200, "Success", data=[history.model_dump() for history in histories])


@router.get("/{message_id}")
async def get_all_messages(message_id: str, user: Annotated[UserSchema, Depends(auth_user_middleware)]):
    messages = await get_messages_by_id(message_id, user)
    return response(200, "Success", data=[msg.model_dump() for msg in messages])
