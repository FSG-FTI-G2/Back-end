from typing import Any
import asyncio
from pydantic import BaseModel, Field
from fastapi import HTTPException
from qdrant_client.http.models import Payload
from app.models.user_schema import UserSchema
from app.models.message_schema import MessageSchema
from app.providers import llm, embedder, vector_db
from app.utils.prompt_template import RolePrompt
from app.utils.logger import get_logger

logger = get_logger("CHAT", color=1)
err_logger = get_logger("CHAT", color=1, type="error")


async def get_all_history(user: UserSchema) -> list[MessageSchema]:
    return MessageSchema.find_messages_by_user_id(user.id)


async def get_messages_by_id(message_id: str, user: UserSchema):
    message = MessageSchema.find_message_by_id(message_id)
    if message.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return message.get_all_messages() if message else []


class GetTitleOutput(BaseModel):
    title: str = Field(...,
                       description="The summarized messages to be used as title")


def __format_context(data: list[Payload]) -> str:
    context = "--- Context ---\n"
    for d in data:
        context += f"File: {d['file_name']}\nContent: {d['content']}\n\n"
    return context + "--- End of Context ---"


async def add_message(message: str, message_id: str | None, role: RolePrompt, user: UserSchema) -> MessageSchema:
    # Create message if message_id is None
    if message_id is None:
        message_instance = MessageSchema(
            user_id=user.id,
            messages=[],
            role_prompt=role or RolePrompt.GENERAL
        ).create()
    # Else, get message by message_id
    else:
        message_instance = MessageSchema.find_message_by_id(message_id)
        if message_instance.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    # Embed message
    embedded_message = embedder.embed(message)[0]

    # Retrieve the vector of the message
    contexts = vector_db.search_vector(user.id, embedded_message)
    for context in contexts:
        logger(f"Context: {context}")

    await llm.response(
        question=message,
        context=__format_context([c.payload for c in contexts]),
        history=message_instance.messages,
        role=message_instance.role_prompt,
    )

    # Check if message not have title
    try:
        if not message_instance.title:
            # Generate title
            title_response = await llm.structured_response(
                f"Recent message: {message_instance.messages[-1].content}", GetTitleOutput, role=RolePrompt.GENERAL)
            message_instance.title = title_response.title
    except Exception as e:
        err_logger(f"Error when create chat title: {e}")
        message_instance.title = "New Chat"

    # Save message
    message_instance.update()

    return message_instance


async def delete_message(message_id: str, user: UserSchema) -> bool:
    message = MessageSchema.find_message_by_id(message_id)
    if message.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return message.delete() > 0


async def mock_response_generator():
    sample_text = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    )

    chunk_size = 50  # Customize the size of each text chunk
    for i in range(0, len(sample_text), chunk_size):
        # await asyncio.sleep(0.2)  # Simulate asynchronous delay
        await asyncio.sleep(0.2)
        text = sample_text[i:i+chunk_size]
        print(f"data: {text}\n\n")
        yield text
