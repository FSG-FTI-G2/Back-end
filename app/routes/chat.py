from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserSchema
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.chat_controller import get_all_history, get_messages_by_id, add_message, delete_message
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


@router.post("/messages")
async def add_new_messages(
    message_data: dict[str, Any],
    user: UserSchema = Depends(auth_user_middleware)
):
    try:
        # Lưu hoặc cập nhật tin nhắn
        message_id = await add_message(user, message_data)
        return response(
            code=status.HTTP_201_CREATED,
            message="Message saved successfully.",
            data={"message_id": message_id}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save message: {str(e)}"
        )


@router.delete("/messages/{message_id}")
async def delete_user_message(
    message_id: str,
    user: UserSchema = Depends(auth_user_middleware)
):
    try:
        is_deleted = await delete_message(user, message_id)
        if is_deleted:
            return response(
                code=status.HTTP_200_OK,
                message="Message deleted successfully.",
                data={"message_id": message_id}
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found."
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete message: {str(e)}"
        )
