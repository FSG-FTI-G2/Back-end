from app.models.user import UserSchema
from app.models.message import MessageSchema


def get_all_history(page_size: int, page_index: int, user: UserSchema):
    return MessageSchema.find_messages_by_user_id(user.id, page_size, page_index)


def get_messages_by_id(message_id: str, user: UserSchema):
    message = MessageSchema.find_message_by_id(message_id, user.id)
    return message.get_all_messages() if message else []
