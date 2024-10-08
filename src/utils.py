import base64
import io
import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

from src.config import COMMON_EXCLUSIONS, VALID_EXTENSIONS

import streamlit as st
import tiktoken
import toml
from streamlit.runtime.uploaded_file_manager import UploadedFile

CONFIG_FILE = "settings.toml"


class Config:
    def __init__(self, filepath: str = CONFIG_FILE) -> None:
        self.filepath = Path(filepath)

    def load(self) -> dict[str, Any]:
        """Loads the configuration from the specified file."""
        try:
            return toml.load(self.filepath)
        except FileNotFoundError:
            return {}
        except toml.TomlDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            return {}

    def save(self, config: dict[str, Any]) -> None:
        """Saves the configuration to the specified file."""
        try:
            with open(self.filepath, "w") as f:
                toml.dump(config, f)
            print(f"Configuration saved successfully to {self.filepath}")
        except OSError as e:
            print(f"Error saving configuration: {e}")

    def update(self, config: dict[str, Any]) -> None:
        """Merges the given configuration with the existing one and saves it."""
        try:
            if config:
                existing_config = self.load()
                existing_config.update(config)
                config_to_save = existing_config
            else:
                config_to_save = config

            with open(self.filepath, "w") as f:
                toml.dump(config_to_save, f)
            print(f"Configuration saved successfully to {self.filepath}")

        except OSError as e:
            print(f"Error saving configuration: {e}")
        except toml.TomlDecodeError as e:
            print(f"Error parsing existing configuration file: {e}")
            print("Saving new configuration without merging.")
            with open(self.filepath, "w") as f:
                toml.dump(config, f)


def apply_global_styles(file_name: str) -> None:
    with open(file_name) as f:
        st.html(f"<style>{f.read()}</style>")


@st.cache_data(show_spinner=False)
def render_image(
    path: Path | str,
    width: str = "50px",
    height: str = "auto",
) -> str:
    """Encodes the given SVG or PNG file to base64."""
    path = path if isinstance(path, Path) else Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Determine the content type based on the file extension
    if path.suffix.lower() == ".svg":
        content_type = "image/svg+xml"
        image_data = path.read_text(encoding="utf-8")
        b64 = base64.b64encode(image_data.encode("utf-8")).decode("utf-8")
    elif path.suffix.lower() == ".png":
        content_type = "image/png"
        with open(path, "rb") as image_file:
            image_data = image_file.read()  # type: ignore
        b64 = base64.b64encode(image_data).decode("utf-8")  # type: ignore
    else:
        raise ValueError("Unsupported file type. Please provide an SVG or PNG file.")

    return f'<img src="data:{content_type};base64,{b64}" style="width: {width}; height: {height};"/>'


def check_api_key(provider_name: str, api_key: str) -> None:
    """Check if the API key is empty or has a placeholder value and print a warning."""
    placeholder_value = f"your_{provider_name}_api_key_here"

    if not api_key or api_key == placeholder_value:
        st.warning(
            f"Warning: The API key for {provider_name} is either empty or set to the placeholder value. Please update it in your configuration."  # noqa: E501
        )


def read_uploaded_files(files_list: list[UploadedFile] | None) -> str:
    """Reads content from multiple uploaded files."""
    buffer = io.StringIO()
    for f in files_list:  # type: ignore
        if f.size > 0:  # Check for empty files
            buffer.write(f"""
                {f.name}:\n\n
                {f.getvalue().decode("utf-8", errors='ignore')}\n\n
                """)
    return buffer.getvalue()


def get_files_by_extensions(directory: Path, exclusions: set[str] = COMMON_EXCLUSIONS) -> Generator[Path, None, None]:
    """Yields files with specified extensions within a directory, skipping excluded directories."""
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclusions]
        for file in files:
            file_path = Path(file)
            if file_path.suffix in VALID_EXTENSIONS:
                yield Path(root) / file_path


def build_folder_tree(directory: Path, exclusions: set[str] = COMMON_EXCLUSIONS, prefix: str = "") -> str:
    """Recursively builds a tree structure of the directory, skipping excluded directories."""
    tree_structure = []

    try:
        items = sorted(directory.iterdir(), key=lambda x: x.name)
    except PermissionError:
        return f"{prefix}Permission Denied"

    for i, item in enumerate(items):
        if item.name in exclusions:
            continue

        connector = "└── " if i == len(items) - 1 else "├── "
        if item.is_dir():
            tree_structure.append(f"{prefix}{connector}{item.name}/")
            sub_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
            tree_structure.append(build_folder_tree(item, exclusions, sub_prefix))
        elif item.suffix in VALID_EXTENSIONS:
            tree_structure.append(f"{prefix}{connector}{item.name}")

    return "\n".join(tree_structure)


def process_folder(directory_path: str, exclusions: set[str] = COMMON_EXCLUSIONS) -> tuple[list[str], str]:
    """Processes the directory and returns a list of relevant files and a tree structure."""
    directory = Path(directory_path)

    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Directory not found or is not a directory: {directory}")

    relevant_files = list(get_files_by_extensions(directory, exclusions))
    folder_tree = build_folder_tree(directory, exclusions) if relevant_files else "No relevant files found."

    return [str(file) for file in relevant_files], folder_tree


def concatenate_file_contents(files_list: list) -> str:
    """Reads content from multiple paths to files and concatenates them into one string."""
    buffer = io.StringIO()

    for file_path in files_list:
        path = Path(file_path)

        if path.exists() and path.is_file() and path.stat().st_size > 0:
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
                buffer.write(f"{path.name}:\n\n{content}\n\n")

    return buffer.getvalue()


@st.cache_data
def get_encoding(encoding_name: str) -> tiktoken.Encoding:
    """Retrieve and cache the encoding based on the encoding name."""
    return tiktoken.get_encoding(encoding_name)


def estimate_token_count(text: str, encoding_name: str | None = "cl100k_base") -> int:
    """
    Estimate the number of tokens in the input text using the specified encoding.

    Args:
        text (str): The text to encode.
        encoding_name (Optional[str], optional): The encoding name (default is "cl100k_base").

    Returns:
        int: Estimated number of tokens.

    Raises:
        TypeError: If `text` or `encoding_name` is not a string.
        ValueError: If `encoding_name` is unrecognized.
    """
    # Validate input types
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(encoding_name, str):
        raise TypeError("Encoding name must be a string.")

    # Use cached encoding retrieval
    encoding = get_encoding(encoding_name)

    return len(encoding.encode(text))
