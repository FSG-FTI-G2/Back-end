import enum
from typing import TypeVar, Type, TypedDict, Literal, List, Generator, Callable, Coroutine
from typing_extensions import deprecated
from pydantic import BaseModel
from fastapi import HTTPException
from llama_index.core.llms import ChatMessage, LLM, MessageRole
from typing import Dict, Any
from app.utils.prompt_template import RolePrompt, get_prompt_by_role
from app.configs.llm import GPTClient, GeminiClient


_T = TypeVar("T", bound=BaseModel)


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


class LLMModel(str, enum.Enum):
    GPT = "gpt"
    GEMINI = "gemini"
    OLLAMA = "ollama"


DEFAULT_MODEL = LLMModel.GEMINI
DEFAULT_ROLE = RolePrompt.STUDENT


class LLMProvider:
    def __init__(self): ...

    def __get_llm_model(self, model: LLMModel) -> LLM:
        if model == LLMModel.GPT:
            return GPTClient
        elif model == LLMModel.GEMINI:
            return GeminiClient
        # elif model == LLMModel.OLLAMA:
        #     return OllamaClient
        else:
            raise HTTPException(
                status_code=400, detail="Invalid model name")

    def __parse_gemini_raw_response(self, raw: GeminiNativeResponse) -> str:
        return raw["content"]["parts"][0]["text"]

    def __system_message(self, role: RolePrompt) -> ChatMessage:
        return ChatMessage.from_str(get_prompt_by_role(role), role=MessageRole.SYSTEM)

    def __prune_history(self, history: list[ChatMessage], max_history: int) -> list[ChatMessage]:
        return history[-max_history:]

    async def structured_response(
        self,
        question: str,
        parser: Type[_T],
        history: list[ChatMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None
    ) -> _T:
        # Select the LLM
        selected_llm = self.__get_llm_model(model_name)

        # Convert the LLM to a structured LLM
        sllm = selected_llm.as_structured_llm(output_cls=parser)

        # Prune the history
        if max_history:
            history = self.__prune_history(history, max_history)
        history.append(ChatMessage.from_str(question))

        # Chat with the LLM
        output = await sllm.achat([self.__system_message(role), *history])
        history.append(output.message)
        return output.raw

    @deprecated("Structured streaming is not supported yet by Llama-Index")
    def stream_structured_response(
        self,
        question: str,
        parser: Type[_T],
        history: list[ChatMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
        callback: Callable = None
    ) -> Generator:
        # Select the LLM
        selected_llm = self.__get_llm_model(model_name)

        # Convert the LLM to a structured LLM
        sllm = selected_llm.as_structured_llm(output_cls=parser)

        # Prune the history
        if max_history:
            history = self.__prune_history(history, max_history)
        history.append(ChatMessage.from_str(question))

        # Chat with the LLM
        historical = False
        gen = sllm.stream_chat([self.__system_message(role), *history])
        for output in gen:
            if historical:
                history[-1].content = output.message.content
            else:
                history.append(output.message)
                historical = True
            yield output.raw

        # Callback
        if callback:
            callback()

    async def response(
        self,
        question: str,
        history: list[ChatMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
    ) -> str:
        # Select the LLM
        selected_llm = self.__get_llm_model(model_name)

        # Prune the history
        if max_history:
            history = self.__prune_history(history, max_history)
        history.append(ChatMessage.from_str(question))

        # Chat with the LLM
        output = await selected_llm.achat(
            [self.__system_message(role), *history])
        history.append(output.message)
        return output.message.content

    def stream_response(
        self,
        question: str,
        history: list[ChatMessage] = [],
        role: RolePrompt = DEFAULT_ROLE,
        model_name: LLMModel = DEFAULT_MODEL,
        max_history: int = None,
        callback: Callable = None
    ) -> Generator:
        # Select the LLM
        selected_llm = self.__get_llm_model(model_name)

        # Prune the history
        if max_history:
            history = self.__prune_history(history, max_history)
        history.append(ChatMessage.from_str(question))

        # Chat with the LLM
        historical = False
        gen = selected_llm.stream_chat([self.__system_message(role), *history])
        for output in gen:
            if historical:
                history[-1].content = output.message.content
            else:
                history.append(output.message)
                historical = True
            yield output.message.content

        # Callback
        if callback:
            callback()
