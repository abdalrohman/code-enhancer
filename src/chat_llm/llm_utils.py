from typing import Any

from src.chat_llm.exceptions import InputValidationError, LLMConfigurationError, LLMError, LLMRuntimeError
from src.chat_llm.llm_config import LLMConfig, OutputMode
from src.chat_llm.llm_factory import LLMFactory, OutputParserFactory
from src.chat_llm.llm_handler import DefaultLLMHandler

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BaseChatPromptTemplate
from langchain_core.runnables import RunnableSerializable


def configure_llm_call(
    config: LLMConfig,
    prompt: BaseChatPromptTemplate,
    output_mode: OutputMode | str = OutputMode.STRING,
    custom_output_parser: BaseOutputParser | None = None,
) -> RunnableSerializable:
    """
    Configure and return a runnable LLM call.

    Args:
        config (LLMConfig): The LLM configuration.
        prompt (BaseChatPromptTemplate): The prompt template for the LLM.
        output_mode (Union[OutputMode, str]): The desired output format.
        custom_output_parser (Optional[BaseOutputParser]): A custom output parser for CUSTOM mode.

    Returns:
        RunnableSerializable: A runnable object representing the configured LLM call.

    Raises:
        LLMConfigurationError: If there's an error in LLM configuration.
        ValueError: If the input parameters are invalid.
    """
    if not prompt:
        raise ValueError("Prompt is required.")
    if not config.api_key:
        raise ValueError("API key is required.")

    try:
        llm = LLMFactory.create_llm(config)
        output_parser = OutputParserFactory.get_parser(output_mode, custom_output_parser)
        return llm | output_parser
    except LLMError:
        raise
    except Exception as e:
        raise LLMConfigurationError(f"Unexpected error occurred: {e!s}")


def get_llm_response(
    config: LLMConfig,
    system_prompt: BaseChatPromptTemplate,
    user_message: dict[str, str],
    output_mode: OutputMode | str = OutputMode.STRING,
    custom_output_parser: BaseOutputParser | None = None,
) -> Any:  # noqa: ANN401
    """
    Get a response from the LLM based on the provided configuration and input.

    Args:
        config (LLMConfig): The LLM configuration.
        system_prompt (BaseChatPromptTemplate): The system prompt template.
        user_message (Dict[str, str]): The user's input message.
        output_mode (Union[OutputMode, str]): The desired output format.
        custom_output_parser (Optional[BaseOutputParser]): A custom output parser for CUSTOM mode.

    Returns:
        Union[str, Dict, List]: The LLM response in the specified format.

    Raises:
        LLMError: If there's any error during the LLM interaction process.
    """

    if not system_prompt:
        raise InputValidationError("System prompt is required.")
    if not isinstance(user_message, dict):
        raise InputValidationError("User message must be a dict")

    try:
        handler = DefaultLLMHandler(config, system_prompt, output_mode, custom_output_parser)
        return handler.process(user_message)
    except LLMError:
        raise
    except Exception as e:
        raise LLMRuntimeError(f"Unexpected error occurred while getting LLM response: {e!s}")
