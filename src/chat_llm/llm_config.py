from enum import Enum

from langchain_core.callbacks import BaseCallbackManager


class OutputMode(Enum):
    """Enumeration of supported output modes."""

    JSON = "json"
    STRING = "str"
    CUSTOM = "custom"


class LLMConfig:
    """Configuration class for LLM settings."""

    def __init__(
        self,
        model: str,
        model_provider: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        base_url: str | None = None,
        callback_manager: BaseCallbackManager | None = None,
        streaming: bool = False,
        stop: list[str] | None = None,
    ):
        self.model = model
        self.model_provider = model_provider
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url
        self.callback_manager = callback_manager
        self.streaming = streaming
        self.stop = stop
