from typing import List
from pydantic import Field
from llama_index.core.llms import ChatMessage
from app.models.base import BaseSchema
from app.providers import message_db


class MessageSchema(BaseSchema):
    title: str = Field(None, alias="title")
    user_id: str = Field(None, alias="user_id")
    messages: List[ChatMessage] = Field(default_factory=list, alias="messages")

    @staticmethod
    def find_messages_by_user_id(user_id: str, page_size: int, page_index: int) -> List['MessageSchema']:
        data = message_db.query({"user_id": user_id}, page_size, page_index)
        return [MessageSchema.model_validate(item) for item in data]

    def search_in_messages(self, keyword: str, page_size: int, page_index: int) -> List[ChatMessage]:
        data = message_db.query(
            {"messages.content": {"$regex": keyword, "$options": "i"}},
            page_size,
            page_index
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

    def add_message(self, message: str | ChatMessage, add_manual: bool = False) -> None:
        # Add message if not added manually
        # Else, the message are add in LLMProvider by reference
        if add_manual:
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
