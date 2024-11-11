import unittest
from pydantic import BaseModel, Field
from app.providers import llm
import logging
import sys
import asyncio


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class OutputFormat(BaseModel):
    answer: str = Field(..., description="The answer of provided question")
    thought: str = Field(..., description="Thought of the model")


class TestLLMProvider(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __structure_llm(self, question: str, history: list):
        response = await llm.structured_response(
            question, parser=OutputFormat, history=history)
        return response

    async def __unstructure_llm(self, question: str, history: list):
        response = await llm.response(question, history=history)
        return response

    async def test_structure_llm(self):
        history = []

        # Test structured_response, question 1
        question = "What is the capital of France?"
        answer = await self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        logger.info(f"Answer: {answer.answer}")

        # Test structured_response, question 2
        question = "What is question I just asked?"
        answer = await self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        self.assertEqual(answer.answer, "What is the capital of France?")
        logger.info(f"Answer: {answer.answer}")

    async def test_unstructure_llm(self):
        history = []

        # Test response, question 1
        question = "What is the capital of Vietnam?"
        answer = await self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        logger.info(f"Answer: {answer}")

        # Test response, question 2
        question = "What is question I just asked?"
        answer = await self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        self.assertIn("What is the capital of Vietnam?", answer)
        logger.info(f"Answer: {answer}")