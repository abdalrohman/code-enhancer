from abc import ABC, abstractmethod
from typing import Any

from src.chat_llm.exceptions import InputValidationError, LLMRuntimeError
from src.chat_llm.llm_config import LLMConfig, OutputMode
from src.chat_llm.llm_factory import LLMFactory, OutputParserFactory

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BaseChatPromptTemplate


class LLMHandler(ABC):
    """Abstract base class for LLM handlers."""

    def __init__(
        self,
        config: LLMConfig,
        prompt: BaseChatPromptTemplate,
        output_mode: OutputMode | str = OutputMode.STRING,
        custom_output_parser: BaseOutputParser | None = None,
    ):
        self.config = config
        self.prompt = prompt
        self.output_parser = OutputParserFactory.get_parser(output_mode, custom_output_parser)
        self.llm = LLMFactory.create_llm(config)

    @abstractmethod
    def process(self, user_message: dict[str, str]) -> Any:  # noqa: ANN401
        """
        Process the user message and return the LLM response.

        Args:
            user_message (Dict[str, str]): The user's input message.

        Returns:
            Union[str, Dict, List]: The processed LLM response.

        Raises:
            LLMRuntimeError: If there's an error during LLM processing.
        """
        pass


class DefaultLLMHandler(LLMHandler):
    """Default implementation of LLMHandler."""

    def process(self, user_message: dict[str, str]) -> Any:  # noqa: ANN401
        """
        Process the user message using the default LLM handling strategy.

        Args:
            user_message (Dict[str, str]): The user's input message.

        Returns:
            Any: The processed LLM response.

        Raises:
            InputValidationError: If the input is invalid.
            LLMRuntimeError: If there's an error during LLM processing.
        """
        self._validate_input(user_message)
        try:
            chain = self.prompt | self.llm | self.output_parser
            return chain.invoke(user_message)
        except InputValidationError:
            raise
        except Exception as e:
            raise LLMRuntimeError(f"Error processing LLM request: {e!s}")

    def _validate_input(self, user_message: dict[str, str]) -> None:
        """
        Validate the user input against the prompt requirements.

        Args:
            user_message (Dict[str, str]): The user's input message.

        Raises:
            InputValidationError: If required variables are missing from the input.
        """
        prompt_variables = set(self.prompt.input_variables)
        missing_vars = prompt_variables - set(user_message.keys())
        if missing_vars:
            raise InputValidationError(f"Missing variables in user_message: {missing_vars}")
