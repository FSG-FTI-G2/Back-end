import enum
from typing import TypeVar, Type, TypedDict, Literal, List, Generator, Callable, Dict
from pydantic import BaseModel
from typing_extensions import deprecated
from fastapi import HTTPException
from langchain.schema import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain.llms import BaseLLM
from app.utils.prompt_template import RolePrompt, get_prompt_by_role
from app.configs.llm import GPTClient, GeminiClient, OllamaClient
from app.utils.logger import get_logger

_T = TypeVar("T", bound=BaseModel)
logger = get_logger("LLM", color=96)

# Define the response schema for Gemini
class GeminiNativeResponse(TypedDict):
    content: Dict[Literal["parts"], List[Dict[Literal["text"], str]]]
    finish_reason: int
    index: int
    safety_ratings: List
    token_count: int
    grounding_attributions: List
    block_reason: int
    usage_metadata: Dict[Literal["prompt_token_count"] |
                         Literal["candidates_token_count"] | Literal["total_token_count"], int]

# Enum for model selection
class LLMModel(str, enum.Enum):
    GPT = "gpt"
    GEMINI = "gemini"
    OLLAMA = "ollama"

# Default settings
DEFAULT_MODEL = LLMModel.GEMINI
DEFAULT_ROLE = RolePrompt.EXPERT

# Wrappers for each client to standardize the response format
class GPTClientWrapper(BaseLLM):
    async def agenerate(self, messages: List[BaseMessage]) -> str:
        prompt = "\n".join([msg.content for msg in messages])
        return await GPTClient().generate(prompt)

class GeminiClientWrapper(BaseLLM):
    async def agenerate(self, messages: List[BaseMessage]) -> str:
        prompt = "\n".join([msg.content for msg in messages])
        return await GeminiClient().generate(prompt)

class OllamaClientWrapper(BaseLLM):
    async def agenerate(self, messages: List[BaseMessage]) -> str:
        prompt = "\n".join([msg.content for msg in messages])
        return await OllamaClient().generate(prompt)

# Main provider class for LLM selection and structured response handling
class LLMProvider:
    def __init__(self): ...

    def __get_llm_model(self, model: LLMModel) -> BaseLLM:
        if model == LLMModel.GPT:
            return GPTClientWrapper()
        elif model == LLMModel.GEMINI:
            return GeminiClientWrapper()
        elif model == LLMModel.OLLAMA:
            return OllamaClientWrapper()
        else:
            raise HTTPException(status_code=400, detail="Invalid model name")

    def __system_message(self, role: RolePrompt) -> SystemMessage:
        return SystemMessage(content=get_prompt_by_role(role))

    def __prune_history(self, history: List[BaseMessage], max_history: int) -> List[BaseMessage]:
        return history[-max_history:] if max_history else history

    async def structured_response(
        self,
        question: str,
        parser: Type[_T],
        context: str = None,
        history: List[BaseMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None
    ) -> _T:
        # Select the LLM model
        selected_llm = self.__get_llm_model(model_name)

        # Prune the history if needed
        if max_history:
            history = self.__prune_history(history, max_history)
        
        # Add the new question to history
        history.append(HumanMessage(content=question))
        new_message = HumanMessage(content=f"{context or ''} Prompt: {question}")

        # Format the messages and send to LLM
        messages = [self.__system_message(role), *history[:-1], new_message]
        output = await selected_llm.agenerate(messages=messages)
        
        # Parse and return the structured response
        history.append(AIMessage(content=output))
        logger(f"Structured response: {output}")
        return parser.parse_raw(output)

    @deprecated("Structured streaming is not supported yet by LangChain")
    def stream_structured_response(
        self,
        question: str,
        parser: Type[_T],
        context: str = None,
        history: List[BaseMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
        callback: Callable = None
    ) -> Generator:
        # Select the LLM
        selected_llm = self.__get_llm_model(model_name)

        # Prune the history if needed
        if max_history:
            history = self.__prune_history(history, max_history)
        
        # Prepare new message and history
        history.append(HumanMessage(content=question))
        new_message = HumanMessage(content=f"{context or ''} Prompt: {question}")

        # Send to LLM with streaming
        messages = [self.__system_message(role), *history[:-1], new_message]
        gen = selected_llm.stream(messages=messages)

        historical = False
        for output in gen:
            if historical:
                history[-1] = AIMessage(content=output)
            else:
                history.append(AIMessage(content=output))
                historical = True
            yield output

        if callback:
            callback()

    async def response(
        self,
        question: str,
        context: str = None,
        history: List[BaseMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
    ) -> str:
        # Select the LLM model
        selected_llm = self.__get_llm_model(model_name)

        # Prune history if needed
        if max_history:
            history = self.__prune_history(history, max_history)
        
        # Add question to history and create message
        history.append(HumanMessage(content=question))
        new_message = HumanMessage(content=f"{context or ''} Prompt: {question}")

        # Send to LLM and get response
        messages = [self.__system_message(role), *history[:-1], new_message]
        output = await selected_llm.agenerate(messages=messages)
        
        # Update history and log
        history.append(AIMessage(content=output))
        logger(f"Response: {output}")
        return output

    def stream_response(
        self,
        question: str,
        context: str = None,
        history: List[BaseMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
        callback: Callable = None
    ) -> Generator:
        # Select the LLM model
        selected_llm = self.__get_llm_model(model_name)

        # Prune history if needed
        if max_history:
            history = self.__prune_history(history, max_history)
        
        # Add question to history and create message
        history.append(HumanMessage(content=question))
        new_message = HumanMessage(content=f"{context or ''} Prompt: {question}")

        # Stream response from LLM
        messages = [self.__system_message(role), *history[:-1], new_message]
        gen = selected_llm.stream(messages=messages)

        historical = False
        for output in gen:
            if historical:
                history[-1] = AIMessage(content=output)
            else:
                history.append(AIMessage(content=output))
                historical = True
            yield output

        if callback:
            callback()
