import unittest
from langchain.schema import BaseMessage
from app.models.message_schema import MessageSchema
from app.providers.llm_provider import MessageRole


class TestMessageSchema(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super(TestMessageSchema, self).__init__(*args, **kwargs)
        # Mock data setup
        self.user_id = "6708c6cc1a071354f0cccb08"
        self.title = "Test Conversation"
        self.message_content = "Hello, this is a test message."

    def __create_message_schema(self):
        message_schema = MessageSchema(
            title=self.title, user_id=self.user_id)
        message_schema.create()
        return message_schema

    def __add_message(self, schema: MessageSchema):
        new_message = BaseMessage(role=MessageRole.USER,
                                  content="Hello, this is a test message.")
        schema.add_message(new_message, add_manual=True)

        new_message = "AI response."
        schema.add_message(new_message, add_manual=True)

        self.assertEqual(len(schema.messages), 2)

    def __get_all_messages(self, schema: MessageSchema):
        messages = schema.get_all_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].content, "Hello, this is a test message.")

    def __find_messages_by_user(self, schema: MessageSchema):
        found_messages = schema.find_messages_by_user_id(
            self.user_id, page_size=10, page_index=0)
        self.assertEqual(len(found_messages), 1)
        self.assertEqual(found_messages[0].title, self.title)

    def __search_messages(self, schema: MessageSchema):
        searched_messages = schema.search_in_messages(
            keyword="test", page_size=10, page_index=0)
        self.assertEqual(len(searched_messages), 1)
        self.assertEqual(searched_messages[0].title, self.title)

    def __delete_messages(self, schema: MessageSchema):
        schema.delete_message(message_index=1)
        self.assertEqual(len(schema.messages), 1)

    def test_message_schema(self):
        # Create a new message schema
        message_schema = self.__create_message_schema()
        self.assertIsNotNone(message_schema.id)

        # Add messages to the schema
        self.__add_message(message_schema)

        # Get all messages
        self.__get_all_messages(message_schema)

        # Find messages by user ID
        self.__find_messages_by_user(message_schema)

        # Search messages
        self.__search_messages(message_schema)

        # Delete messages
        self.__delete_messages(message_schema)
