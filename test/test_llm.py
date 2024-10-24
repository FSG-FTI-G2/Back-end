import unittest
from pydantic import BaseModel, Field
from app.providers import llm
import logging
import sys


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class OutputFormat(BaseModel):
    answer: str = Field(..., description="Answer of question")
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

    async def __stream_unstructure_llm(self, question: str, history: list):
        response_generator = llm.stream_response(question, history=history)
        logger.info("Start streaming response")
        async for response in response_generator:
            logger.info(f"{response}\n------------------")
        logger.info("End streaming response")
        return response

    async def test_structure_llm(self):
        history = []

        # Test structured_response, question 1
        question = "What is the capital of France?"
        answer = await self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        logger.info(f"Answer: {answer.answer}")

        # Test structured_response, question 2
        question = "What question I just asked?"
        answer = await self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        logger.info(f"Answer: {answer.answer}")

    async def test_unstructure_llm(self):
        history = []

        # Test response, question 1
        question = "What is the capital of Vietnam?"
        answer = await self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        logger.info(f"Answer: {answer}")

        # Test response, question 2
        question = "What question I just asked?"
        answer = await self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        logger.info(f"Answer: {answer}")

    async def test_stream_structure_llm(self):
        history = []

        # Test stream_structured_response, question 1
        question = "What is Gemini? Explain more detail about it."
        await self.__stream_unstructure_llm(question, history)

        logger.info(f"History: {history[1]}")
