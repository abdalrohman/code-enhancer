from collections import namedtuple
from enum import Enum

from .prompts import code_enhancer_prompt, markdown_writing_prompt

Provider = namedtuple("Provider", ["provider_name", "api_key_env_var", "models", "base_url"])

prompts_mapping = {
    "code_enhancer_prompt": code_enhancer_prompt,
    "markdown_writing_prompt": markdown_writing_prompt,
}

google_models = [
    # Latest
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    # Latest stable
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    # Stable
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    # Experimental
    "gemini-1.5-pro-exp-0827",
    "gemini-1.5-flash-8b-exp-0924",
    "gemini-1.5-flash-8b-exp-0827",
    "gemini-1.5-flash-exp-0827",
    # Flash 8b
    "gemini-1.5-flash-8b-latest",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-8b-001",
]

github_models = [
    "gpt-4o",
    "gpt-4o-mini",
    "phi-3.5-moe-instruct",
    "phi-3.5-mini-instruct",
    "phi-3.5-vision-instruct",
    "phi-3-medium-instruct-128k",
    "phi-3-medium-instruct-4k",
    "phi-3-mini-instruct-128k",
    "phi-3-mini-instruct-4k",
    "phi-3-small-instruct-128k",
    "phi-3-small-instruct-8k",
    "ai21-jamba-1.5-large",
    "ai21-jamba-1.5-mini",
    "ai21-jamba-instruct",
    "cohere-command-r",
    "cohere-command-r-08-2024",
    "cohere-command-r-plus",
    "cohere-command-r-plus-08-2024",
    "llama-3.2-11b-vision-instruct",
    "llama-3.2-90b-vision-instruct",
    "meta-llama-3.1-405b-instruct",
    "meta-llama-3.1-70b-instruct",
    "meta-llama-3.1-8b-instruct",
    "meta-llama-3-70b-instruct",
    "meta-llama-3-8b-instruct",
    "mistral-nemo",
    "mistral-large",
    "mistral-large-2407",
    "mistral-small",
]

cohere_models = [
    "command-r",
    "command-r-plus",
    "command-light-nightly",
    "command-nightly",
    "command",
    "command-r-08-2024",
    "command-r-plus-08-2024",
    "command-light",
]

groq_models = [
    "llama3-8b-8192",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "llama3-70b-8192",
    "llama-3.2-3b-preview",
    "llama-3.1-70b-versatile",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama-3.2-90b-text-preview",
    "mixtral-8x7b-32768",
    "llama-3.2-1b-preview",
    "llama-guard-3-8b",
    "llama-3.2-11b-vision-preview",
    "gemma-7b-it",
    "llama3-groq-8b-8192-tool-use-preview",
    "llama-3.2-11b-text-preview",
]

openai_models = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-3.5-turbo",
    "o1-preview",
    "o1-mini",
]

ollama_models = [
    "llama3.2:1b",
    "phi3.5:latest",
    "gemma2:2b",
]

together_models = [
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    "meta-llama/Llama-3.2-3B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    "meta-llama/Meta-Llama-3-70B-Instruct-Lite",
    "meta-llama/Llama-3-8b-chat-hf",
    "meta-llama/Llama-3-70b-chat-hf",
    "microsoft/WizardLM-2-8x22B",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "databricks/dbrx-instruct",
    "deepseek-ai/deepseek-llm-67b-chat",
    "google/gemma-2b-it",
    "Gryphe/MythoMax-L2-13b",
    "meta-llama/Llama-2-13b-chat-hf",
    "mistralai/Mistral-7B-Instruct-v0.1",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "togethercomputer/StripedHyena-Nous-7B",
    "upstage/SOLAR-10.7B-Instruct-v1.0",
]

PROVIDER_DICT = {
    "github_models": Provider("openai", "GITHUB_API_KEY", github_models, "https://models.inference.ai.azure.com"),
    "google_genai": Provider("google_genai", "GOOGLE_API_KEY", google_models, None),
    "cohere": Provider("cohere", "COHERE_API_KEY", cohere_models, "https://api.cohere.com/v1"),
    "groq": Provider("groq", "GROQ_API_KEY", groq_models, None),
    "anthropic": Provider("anthropic", "ANTHROPIC_API_KEY", ["claude-3-5-sonnet-20240620"], None),
    "openai": Provider("openai", "OPENAI_API_KEY", openai_models, None),
    "together": Provider("together", "TOGETHER_API_KEY", together_models, "https://api.together.ai/v1/"),
    "ollama": Provider("ollama", "", ollama_models, None),
}


# TODO add more programming languages
PROGRAMMING_LANGUAGE_CONFIG = {
    "Python": {
        "extensions": {".py", ".pyw", ".pyi"},
        "exclusions": {
            ".mypy_cache",
            ".ruff_cache",
            "__pycache__",
            ".pytest_cache",
            "*.egg-info",
            "*.whl",
            "venv",
            "env",
            ".ipynb",
        },
    },
    "JavaScript": {
        "extensions": {".js", ".jsx", ".ts", ".tsx"},
        "exclusions": {
            "node_modules",
            ".next",
            "build",
            "dist",
            "*.log",
        },
    },
    "C++": {"extensions": {".cpp", ".h", ".hpp", ".c", ".cc"}, "exclusions": {"bin", "obj", "*.o", "*.exe"}},
    "CSS": {"extensions": {".css", ".scss", ".sass"}, "exclusions": {"node_modules", "build", "*.map"}},
    "HTML": {"extensions": {".html", ".htm"}, "exclusions": {"node_modules", "dist"}},
    "Git": {"exclusions": {".git"}},
    "Java": {"extensions": {".java", ".class"}, "exclusions": {"target", "*.jar", "*.war", "*.ear"}},
    "Ruby": {"extensions": {".rb"}, "exclusions": {"*.gem", ".bundle", "log", "tmp"}},
    "PHP": {"extensions": {".php"}, "exclusions": {"vendor", "*.log", "*.cache"}},
    "Go": {"extensions": {".go"}, "exclusions": {"vendor", "*.test", "*.out"}},
    "Swift": {"extensions": {".swift"}, "exclusions": {"*.xcodeproj", "*.xcworkspace", "*DerivedData*"}},
    "Kotlin": {"extensions": {".kt", ".kts"}, "exclusions": {"build", "*.jar"}},
    "TypeScript": {"extensions": {".ts", ".tsx"}, "exclusions": {"node_modules", ".next", "*.log"}},
    "Rust": {"extensions": {".rs"}, "exclusions": {"target", "*.rs.bk"}},
    "Env": {"exclusions": {".env"}},
}


VALID_EXTENSIONS = {ext for config in PROGRAMMING_LANGUAGE_CONFIG.values() for ext in config.get("extensions", [])}
COMMON_EXCLUSIONS = set().union(*(config.get("exclusions", {}) for config in PROGRAMMING_LANGUAGE_CONFIG.values()))


class Emoji(Enum):
    CODE_SYMBOL = "💻"
    ENHANCE_ACTION = "🌟"

    # Configuration
    CONFIG_SECTION = "⚙️"
    AI_PROVIDER = "🏢"
    AI_MODEL = "🧠"
    TEMPERATURE = "🌡️"
    MAX_TOKENS = "📏"
    API_KEY = "🔑"
    BASE_URL = "🔗"

    # User Input and Output
    USER_INPUT = "✍️"
    AI_RESPONSE = "💬"
    OPTIMIZATION_RESULT = "🎯"

    # Actions
    SAVE_CONFIG = "💾"
    RESET_CONFIG = "🔄"
    AUTO_SAVE = "🔁"

    # Tabs and Sections
    ENHANCE_TAB = "🛠️"
    CONFIGURE_TAB = "⚙️"
    ABOUT_TAB = "📖"
    ADVANCED_SETTINGS = "🔬"
    CURRENT_CONFIG = "📊"

    # System Information
    OS_INFO = "🖥️"
    PROCESSOR_INFO = "⚡"
    MEMORY_INFO = "🧠"
    PYTHON_INFO = "🐍"

    # Miscellaneous
    WARNING = "⚠️"
    SUCCESS = "✅"
    ALERT = "📢"
    INFO = "💡"
    HEART = "❤️"

    # Additional Emojis
    PROMPT = "📝"
    HISTORY = "📜"
    ANALYSIS = "🔍"
    LOADING = "⏳"
    ERROR = "❌"
    CREDITS = "🏆"
    LICENSE = "📄"
    VERSION = "🔢"
    DEVELOPER = "👨‍💻"
    DESCRIPTION = "📚"
    NAME = "🆔"
    LANGCHAIN = "🦜🔗"
