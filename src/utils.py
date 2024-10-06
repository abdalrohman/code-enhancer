import base64
from pathlib import Path
from typing import Any

import streamlit as st
import toml

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
