import unittest
from fastapi.testclient import TestClient
from main import app
from langchain.schema import BaseMessage
from app.models.message_schema import MessageSchema
from app.providers.llm_provider import MessageRole


class TestViewHistory(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestViewHistory, self).__init__(*args, **kwargs)
        self.client = TestClient(app)

        # Request login to get token
        response = self.client.post("/api/v1/auth/login", data={
            "username": "admin",
            "password": "admin1111",
        }).json()
        token = response.get("data", {}).get("token")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        # Get user_id from me
        response = self.client.get("/api/v1/auth/me").json().get("data")

        # Tạo cuộc trò chuyện qua endpoint POST để có unique_id
        user_id = response.get("id")
        title = "Test Message"
        messages = [
            BaseMessage(role=MessageRole.USER, content="Hello! Hihi Hahaa?"),
            BaseMessage(role=MessageRole.ASSISTANT,
                        content="I would like to haha hihi."),
            BaseMessage(role=MessageRole.USER,
                        content="Sure! We offer a variety of services, including..."),
        ]
        message = MessageSchema(
            title=title, user_id=user_id, messages=messages).create()
        self.message_id = message.id

    def test_get_all_chat_history(self):
        response = self.client.get("/api/v1/chat/").json()
        self.assertEqual(response.get("code"), 200)
        self.assertIsInstance(response.get("data"), list)

    def test_get_chat_messages(self):
        response = self.client.get(f"/api/v1/chat/{self.message_id}").json()
        self.assertEqual(response.get("code"), 200)
        self.assertIsInstance(response.get("data"), list)
