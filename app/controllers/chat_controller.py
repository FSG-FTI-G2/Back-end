from fastapi import HTTPException
from app.models.user import UserSchema
from app.models.message import MessageSchema


async def get_all_history(user: UserSchema) -> list[MessageSchema]:
    return MessageSchema.find_messages_by_user_id(user.id)


async def get_messages_by_id(message_id: str, user: UserSchema):
    message = MessageSchema.find_message_by_id(message_id)
    if message.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return message.get_all_messages() if message else []
