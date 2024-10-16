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


class TestLLMProvider(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __structure_llm(self, question: str, history: list):
        response = llm.structured_response(
            question, parser=OutputFormat, history=history)
        logger.info(f"Response: {response}")
        return response

    def __unstructure_llm(self, question: str, history: list):
        response = llm.response(question, history=history)
        logger.info(f"Response: {response}")
        return response

    def test_structure_llm(self):
        history = []

        # Test structured_response, question 1
        question = "What is the capital of France?"
        answer = self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        logger.info(f"Answer: {answer.answer}")

        # Test structured_response, question 2
        question = "What question I just asked?"
        answer = self.__structure_llm(question, history)
        self.assertIsInstance(answer, OutputFormat)
        logger.info(f"Answer: {answer.answer}")

    def test_unstructure_llm(self):
        history = []

        # Test response, question 1
        question = "What is the capital of Vietnam?"
        answer = self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        logger.info(f"Answer: {answer}")

        # Test response, question 2
        question = "What question I just asked?"
        answer = self.__unstructure_llm(question, history)
        self.assertIsInstance(answer, str)
        logger.info(f"Answer: {answer}")
