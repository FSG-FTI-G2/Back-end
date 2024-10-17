from typing import Any
from fastapi import HTTPException, status
from app.models.user import UserSchema
from app.models.message import MessageSchema
from app.providers import messages_db
from llama_index.core.llms import MessageRole


async def get_all_history(user: UserSchema) -> list[MessageSchema]:
    return MessageSchema.find_messages_by_user_id(user.id)


async def get_messages_by_id(message_id: str, user: UserSchema):
    message = MessageSchema.find_message_by_id(message_id)
    if message.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return message.get_all_messages() if message else []


async def add_message(user: UserSchema, message_data: dict[str, Any]) -> str:
    try:
        message_id = message_data.get("message_id")
        prompt = message_data.get("question")

        if not message_id:
            new_message = MessageSchema(
                user_id=str(user.id),
                messages=[{"role": MessageRole.USER, "content": prompt}]
            )
            new_message.create()
        else:
            existing_message = messages_db.get_by_id(message_id)
            if existing_message and existing_message.get("user_id") == str(user.id):

                existing_message_obj = MessageSchema.model_validate(
                    existing_message)
                existing_message_obj.add_message(prompt, add_manual=True)
                messages_db.update(
                    message_id,
                    existing_message_obj.model_dump(by_alias=True)
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Message not found or you do not have permission to modify it."
                )
        return str(message_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save message: {str(e)}"
        )


async def delete_message(user: UserSchema, message_id: str) -> bool:
    try:
        message = messages_db.get_by_id(message_id)
        if message and message.get("user_id") == str(user.id):
            deleted_count = messages_db.delete(id=message_id)
            return deleted_count > 0
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or you do not have permission to delete it."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete message: {str(e)}"
        )
