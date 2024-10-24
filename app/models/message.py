from typing import List, Optional
from pydantic import Field
from llama_index.core.llms import ChatMessage
from app.models.base import BaseSchema
from app.providers import message_db
from app.utils.prompt_template import RolePrompt


# Create a index for user_id
message_db.create_index("user_id")


class MessageSchema(BaseSchema):
    title: Optional[str] = Field(None, alias="title")
    user_id: str = Field(None, alias="user_id")
    messages: List[ChatMessage] = Field(
        default_factory=list, alias="messages")
    role_prompt: RolePrompt = Field(
        default=RolePrompt.STUDENT, alias="role_prompt")

    @staticmethod
    def find_messages_by_user_id(user_id: str) -> List['MessageSchema']:
        data = message_db.query({"user_id": user_id}, exclude=["messages"])
        return [MessageSchema.model_validate(item) for item in data]

    @staticmethod
    def find_message_by_id(message_id: str) -> 'MessageSchema':
        data = message_db.get_by_id(message_id)
        if data is not None:
            return MessageSchema.model_validate(data)
        return None

    def search_in_messages(self, keyword: str, page_size: int, page_index: int) -> List[ChatMessage]:
        data = message_db.query(
            {"messages.content": {"$regex": keyword, "$options": "i"}},
            page_size=page_size,
            page_index=page_index
        )
        return [MessageSchema.model_validate(item) for item in data]

    def create(self):
        super().create()
        created_id = message_db.create(self.model_dump(
            exclude=["id"], mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self):
        super().update()
        return message_db.update(
            self.id,
            self.model_dump(exclude=["id"], mode="json", by_alias=True)
        )

    def delete(self) -> int:
        return message_db.delete(self.id)

    def get_all_messages(self) -> List[ChatMessage]:
        return [ChatMessage.model_validate(msg) for msg in self.messages]

    def add_message(self, message: str | ChatMessage = None) -> None:
        # Add message if not None
        # Else, the message are add in LLMProvider by reference
        if message:
            if isinstance(message, str):
                self.messages.append(ChatMessage.from_str(message))
            else:
                self.messages.append(message)
        # Cập nhật message vào cơ sở dữ liệu
        super().update()
        return message_db.update(
            self.id,
            {"$push": {"messages": self.messages[-1].model_dump()}},
            native_query=True
        )

    def delete_message(self, message_index: int) -> int:
        # Delete message from the list
        self.messages.pop(message_index)
        # Update the message
        super().update()
        return message_db.update(
            self.id,
            {"$set": {"messages": [msg.model_dump()
                                   for msg in self.messages]}},
            native_query=True
        )
