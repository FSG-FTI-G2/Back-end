import unittest 
from fastapi.testclient import TestClient
from bson import ObjectId
from main import app 
from app.models.message import Message, MessageSchema, MessageRole

client = TestClient(app)

class Test_View_History(unittest.TestCase):
    # def __init__(self, *args, **kwargs):
    #     super(Test_View_History, self).__init__(*args, **kwargs)
    #     self.user_id = "user_123_test"
    #     self.title = "Test_view"
    #     self.messages = [
    # Message(role=MessageRole.USER, content="Hello! Hihi Hahaa?"),
    # Message(role=MessageRole.ADMIN, content="I would like to haha hihi."),
    # Message(role=MessageRole.USER, content="Sure! We offer a variety of services, including..."),
    # ] 
    #     self.conversation = MessageSchema(title=self.title, user_id=self.user_id,messages=self.messages)

    #     self.conversation.create()
    #     self.unique_id = self.conversation.id
    
    def setUp(self):
        # Tạo cuộc trò chuyện qua endpoint POST để có unique_id
        self.user_id = "user_123_test"
        self.title = "Test_view"
        self.messages = [
            {"role": MessageRole.USER, "content": "Hello! Hihi Hahaa?"},
            {"role": MessageRole.ADMIN, "content": "I would like to haha hihi."},
            {"role": MessageRole.USER, "content": "Sure! We offer a variety of services, including..."},
        ]

        # Tạo payload cho POST request
        conversation_data = {
            "title": self.title,
            "user_id": self.user_id,
            "messages": self.messages
        }
        
        response = client.post("/api/v1/view/create_conversation", json=conversation_data)
        self.assertEqual(response.status_code, 201)
        self.unique_id = response.json()["unique_id"]
        print("Created Unique ID", self.unique_id)
        
    
        print("Unique ID:", self.unique_id)
        
        response = client.get(f"/api/v1/view/view_history/{self.unique_id}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['content'], "Hello! Hihi Hahaa?")
        self.assertEqual(data[1]['content'], "I would like to haha hihi.")























# from app.models.message import MessageSchema, Message, MessageRole
# import unittest

# class TestViewHistory(unittest.TestCase):
#     def __init__(self, *args, **kwargs):
#         super(TestViewHistory, self).__init__(*args, **kwargs)
#         self.user_id = "user_123_test"
#         self.title = "Test_view"
#         self.messages = [
#     Message(role=MessageRole.USER, content="Hello! Hihi Hahaa?"),
#     Message(role=MessageRole.ADMIN, content="I would like to haha hihi."),
#     Message(role=MessageRole.USER, content="Sure! We offer a variety of services, including..."),
# ]
        
#     def test_view(self):
        
        
#         conversation = MessageSchema(title=self.title, user_id=self.user_id,messages=self.messages)

#         conversation.create()
#         unique_id = conversation.id
        
#         retrieved_conversation = MessageSchema(user_id=self.user_id, title=self.title)
#         all_messages = retrieved_conversation.get_messages_by_id(unique_id)
        
#         # self.assertEqual(len(all_messages), len(self.messages))

#         for i, message in enumerate(all_messages):
#             self.assertEqual(message.role, messages[i].role)
#             self.assertEqual(message.content, messages[i].content)
























# messages = [
#     Message(role=MessageRole.USER, content="Hello! How can I help you?"),
#     Message(role=MessageRole.ADMIN, content="I would like to know more about your services."),
#     Message(role=MessageRole.USER, content="Sure! We offer a variety of services, including..."),
# ]

# conversation = MessageSchema(title="Test", user_id="user_123",messages=messages)

# conversation.create()
# unique_id = conversation.id

# # for msg in messages:
# #     conversation.add_message(msg)

# retrieved_conversation = MessageSchema(user_id="user_123", title="Test")
# all_messages = retrieved_conversation.get_messages_by_id(unique_id)

# print("Retrieved Conversation Messages:")
# for message in all_messages:
#     print(f"{message.role}: {message.content}")