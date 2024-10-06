class LLMError(Exception):
    """Base exception class for LLM-related errors."""


class LLMConfigurationError(LLMError):
    """Exception raised for errors in the LLM configuration."""


class LLMRuntimeError(LLMError):
    """Exception raised for runtime errors during LLM operations."""


class OutputParserError(LLMError):
    """Exception raised for errors related to output parsing."""


class InputValidationError(LLMError):
    """Exception raised for errors in input validation."""
