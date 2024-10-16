from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.models.message import MessageSchema, Message
from typing import List
from bson import ObjectId


router = APIRouter()

@router.post("/create_conversation", status_code=status.HTTP_201_CREATED)
async def create_conversation(conversation: MessageSchema):
    created_conversation = conversation.create()
    return {"unique_id": str(created_conversation.id)}

@router.get("/view_history/{unique_id}", response_model=List[Message])
async def view_history(unique_id: str):
    if not ObjectId.is_valid(unique_id):
        raise HTTPException(status_code=400, detail="Invalid unique_id format")
    
    conversation = MessageSchema(user_id="user_123_test", title="Test_view")
    
    messages = conversation.get_messages_by_id(unique_id=unique_id)
    
    if not messages:
        raise HTTPException(status_code=404, detail="No chat history found for the given unique_id.")
    
    return messages
