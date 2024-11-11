from typing import TypeVar, Type, List, Generator, Callable
from typing_extensions import deprecated
from pydantic import BaseModel
import enum
import json
from fastapi import HTTPException
from langchain_core.runnables import Runnable
from langchain.schema import BaseMessage, AIMessage, HumanMessage, SystemMessage
from app.utils.prompt_template import RolePrompt, get_prompt_by_role
from app.configs.llm_config import gpt, azure_gpt, gemini, ollama
from app.utils.logger import get_logger

_T = TypeVar("T", bound=BaseModel)
logger = get_logger("LLM", color=96)


class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


# Enum for model selection
class LLMModel(str, enum.Enum):
    GPT = "gpt"
    AZURE_GPT = "azure_gpt"
    GEMINI = "gemini"
    OLLAMA = "ollama"


# Default settings
DEFAULT_MODEL = LLMModel.OLLAMA
DEFAULT_ROLE = RolePrompt.GENERAL

PROMPT_STRUCTURE_TEMPLATE = '''
---
Here's a JSON schema to follow:
{schema}

Output a valid JSON object but do not repeat the schema.
Do not include any other information in the output.
'''
FAILED_RESPONSE = "Sorry, I can't answer your question at the moment. Please try again later."



# Wrappers for each client to standardize the response format
class ModelWrapper:
    '''
    Model Wrapper for control response format and output for any LLM model.\n
    This class fixed the drawback of LangChain
    '''
    def __init__(self, model: Runnable, max_retry: int = 1):
        self.model = model
        self.structure_prompt_modifier: _T = None
        self.max_retry = max_retry

    def with_structured_output(self, parser: Type[_T]) -> 'ModelWrapper':
        # If the model has a method with_structured_output, use it
        if 'with_structured_output' in self.model.__dict__ and callable(self.model.__dict__['with_structured_output']):
            self.model = self.model.with_structured_output(parser)
        else:
            # Else, return a model, however, enable structured prompt modifier
            self.structure_prompt_modifier = parser
        return self
    
    def __assign_first_str_field(model_instance: BaseModel, value: str):
        for field_name, field in model_instance.model_fields.items():
            if field.type_ == str:
                setattr(model_instance, field_name, value)
                break  # Stop after the first str field is assigned

    async def __ainvoke(self, messages: List[BaseMessage]) -> str | BaseModel:
        # Modify the last message if needed
        if self.structure_prompt_modifier:
            messages[-1].content += PROMPT_STRUCTURE_TEMPLATE.format(
                schema=self.structure_prompt_modifier.model_json_schema())

        result = await self.model.ainvoke(messages)

        # If the model is structured, parse the output
        if self.structure_prompt_modifier:
            if isinstance(result, str):
                result = json.loads(result)
            return self.structure_prompt_modifier.model_validate(result)
        return result
    
    async def ainvoke(self, messages: List[BaseMessage]) -> str | BaseModel:
        while self.max_retry > 0:
            try:
                return await self.__ainvoke(messages)
            except Exception as e:
                logger(f"{self.model.__class__.__name__} error: {e}. Retrying...")
                self.max_retry -= 1
        
        if self.structure_prompt_modifier:
            return self.__assign_first_str_field(self.structure_prompt_modifier, FAILED_RESPONSE)
        return FAILED_RESPONSE
    
    def __invoke(self, messages: List[BaseMessage]) -> str | BaseModel:
        # Modify the last message if needed
        if self.structure_prompt_modifier:
            messages[-1].content += PROMPT_STRUCTURE_TEMPLATE.format(
                schema=self.structure_prompt_modifier.model_json_schema())
            
        result = self.model.invoke(messages)
        
        # If the model is structured, parse the output
        if self.structure_prompt_modifier:
            if isinstance(result, str):
                result = json.loads(result)
            return self.structure_prompt_modifier.model_validate(result)
        return result
    
    def invoke(self, messages: List[BaseMessage]) -> str | BaseModel:
        while self.max_retry > 0:
            try:
                return self.__invoke(messages)
            except Exception as e:
                logger(f"{self.model.__class__.__name__} error: {e}. Retrying...")
                self.max_retry -= 1

        if self.structure_prompt_modifier:
            return self.__assign_first_str_field(self.structure_prompt_modifier, FAILED_RESPONSE)
        return FAILED_RESPONSE



# Main provider class for LLM selection and structured response handling
class LLMProvider:
    def __init__(self): ...

    def __get_llm_model(self, model: LLMModel) -> ModelWrapper:
        if model == LLMModel.GPT:
            return ModelWrapper(gpt)
        elif model == LLMModel.AZURE_GPT:
            return ModelWrapper(azure_gpt)
        elif model == LLMModel.GEMINI:
            return ModelWrapper(gemini, max_retry=2)
        elif model == LLMModel.OLLAMA:
            return ModelWrapper(ollama, max_retry=5)
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
        structured_llm = selected_llm.with_structured_output(parser)

        # Prune the history if needed
        if max_history:
            history = self.__prune_history(history, max_history)

        # Add the new question to history
        history.append(HumanMessage(content=question))
        new_message = HumanMessage(
            content=f"{context or ''}\nPrompt: {question}")

        # Format the messages and send to LLM
        messages = [self.__system_message(role), *history[:-1], new_message]
        output = await structured_llm.ainvoke(messages)

        # Parse and return the structured response
        history.append(AIMessage(content=str(output)))
        logger(f"Structured response: {output}")
        return output

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
        new_message = HumanMessage(
            content=f"{context or ''} Prompt: {question}")

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
        new_message = HumanMessage(
            content=f"{context or ''} Prompt: {question}")

        # Send to LLM and get response
        messages = [self.__system_message(role), *history[:-1], new_message]
        output = await selected_llm.ainvoke(messages=messages)

        # Update history and log
        history.append(AIMessage(content=output))
        logger(f"Response: {output}")
        return output

    @deprecated("Streaming is not supported yet by LangChain")
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
        new_message = HumanMessage(
            content=f"{context or ''} Prompt: {question}")

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
