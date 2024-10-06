from src.chat_llm.exceptions import LLMConfigurationError, OutputParserError
from src.chat_llm.llm_config import LLMConfig, OutputMode

from langchain.chat_models.base import BaseChatModel, init_chat_model
from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser, StrOutputParser


class OutputParserFactory:
    """Factory class for creating output parsers."""

    @staticmethod
    def get_parser(
        output_mode: OutputMode | str,
        custom_parser: BaseOutputParser | None = None,
    ) -> BaseOutputParser:
        """
        Get the appropriate output parser based on the output mode.

        Args:
            output_mode (Union[OutputMode, str]): The desired output mode.
            custom_parser (Optional[BaseOutputParser]): A custom parser for CUSTOM mode.

        Returns:
            BaseOutputParser: The selected output parser.

        Raises:
            OutputParserError: If an invalid output mode is provided or a custom parser is missing.
        """

        if isinstance(output_mode, str):
            output_mode = OutputMode(output_mode.lower())

        match output_mode:
            case OutputMode.JSON:
                return JsonOutputParser()
            case OutputMode.STRING:
                return StrOutputParser()
            case OutputMode.CUSTOM:
                if custom_parser is None:
                    raise OutputParserError("Custom output parser must be provided when using CUSTOM output mode.")
                return custom_parser
            case _:
                raise OutputParserError(f"Invalid output mode: {output_mode}")


class LLMFactory:
    """Factory class for creating LLM instances."""

    @staticmethod
    def create_llm(config: LLMConfig) -> BaseChatModel:
        """
        Create and initialize an LLM instance based on the provided configuration.

        Args:
            config (LLMConfig): The configuration for the LLM.

        Returns:
            BaseChatModel: The initialized LLM instance.

        Raises:
            LLMConfigurationError: If there's an error in LLM initialization.
        """
        try:
            return init_chat_model(
                model=config.model,
                model_provider=config.model_provider,
                api_key=config.api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                base_url=config.base_url,
                callback_manager=config.callback_manager,
                streaming=config.streaming,
                stop=config.stop,
            )
        except Exception as e:
            raise LLMConfigurationError(f"Failed to initialize LLM: {e!s}")
