from typing import List 
from pydantic import Field
from app.models.base import BaseSchema  
from app.providers import message_db  


class Message(BaseSchema):
    role: enumerate = Field(None, alias="role")
    content: str = Field(None, alias= "content")


class MessageSchema(BaseSchema):
    title: str = Field(None, alias= "title")
    user_id: str = Field(None, alias="user_id")
    messages: List[Message] = Field(default_factory=list, alias= "messages")

    @staticmethod
    def add_message(self, message: Message) -> None:
    # Add message
        self.messages.append(message)
    # Update message
        update_count = message_db.update(
            {"user_id": self.user_id, "title": self.title},
            {"$push": {"messages": message.model_dump(exclude_none=True, mode="json", by_alias=True)}}
        )
        if update_count == 0:
            print("Failed to add message. No matching conversation found.")
    
    def get_all_messages(self) -> List['Message']:
    # Get all messages in a conversation
        data = message_db.query({"user_id": self.user_id, "title": self.title})
        if data:
           return [Message(**msg) for msg in data.get("messages", [])]
        return []

    def find_messages_by_user(self, user_id: str, page_size: int, page_index: int) -> List['MessageSchema']:
        # Find messages from a specific user
        data = message_db.query({"user_id": user_id}, page_size, page_index)
        # Validate the data
        return [MessageSchema.model_validate(item) for item in data]
    
    def search_messages(self, keyword: str, page_size: int, page_index: int) -> List['Message']:
        # Find messages containing a certain keyword
        data = message_db.query({"keyword": keyword}, page_size, page_index)
        # Validate the data
        return [MessageSchema.model_validate(item) for item in data]
    
    def delete_messages(self, title: str) -> int:
    # Delete all message in chat
        deleted_count = message_db.delete({"title": title})
        
        if deleted_count > 0:
            print(f"Deleted {deleted_count} messages with title '{title}'.")
        else:
            print(f"No messages found with title '{title}'.")

        return deleted_count

