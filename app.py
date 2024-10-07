import os
import platform
import sys
import textwrap
from typing import Any

from src.chat_llm.llm_config import LLMConfig
from src.chat_llm.llm_utils import get_llm_response
from src.config import PROVIDER_DICT, Emoji, prompts_mapping
from src.utils import (
    Config,
    apply_global_styles,
    check_api_key,
    concatenate_file_contents,
    process_folder,
    read_uploaded_files,
    render_image,
)

import psutil
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(".env")

author_name = "M.Abdulrahman Alnaseer"
version = "0.1.0"
github_link = "https://www.github.com/abdalrohman"

# Page configuration
st.set_page_config(
    page_title="Code Enhancer",
    page_icon="logo/logo.svg",
    layout="wide",
)
st.logo("logo/logo.svg", link=github_link)

# Initialize session state and config
if "enhancement_history" not in st.session_state:
    st.session_state.enhancement_history = []

config = Config()
if "config" not in st.session_state:
    st.session_state.config = config.load()

# Apply custom css file
apply_global_styles("style.css")


def main_tab() -> None:
    st.subheader(f"{Emoji.CONFIG_SECTION.value} Current Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"{Emoji.AI_PROVIDER.value} AI Provider: {st.session_state.config.get('llm_provider', 'Not set')}")
    with col2:
        st.info(f"{Emoji.AI_MODEL.value} AI Model: {st.session_state.config.get('llm_model', 'Not set')}")

    check_api_key(
        provider_name=st.session_state.config.get("llm_provider", ""),
        api_key=st.session_state.config.get("api_key", ""),
    )

    prompts_list = list(prompts_mapping.keys())
    default_system_prompt = st.selectbox("System Prompt", prompts_list)

    with st.expander(f"{Emoji.OPTIMIZATION_RESULT.value} Optimization Prompt (Click to expand/collapse)", expanded=False):
        system_prompt = st.text_area(
            "Customize your optimization prompt:",
            prompts_mapping[default_system_prompt],
            height=300,
        )
        st.info(
            f"{Emoji.INFO.value} Tip: Modify this prompt if you need optimization for a specific programming language or have unique requirements."  # noqa: E501
        )

    # User input
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "File Upload", "Folder Upload"],
        horizontal=True,
    )
    if input_method == "Text Input":
        code_snippet = st.text_area(f"{Emoji.USER_INPUT.value} Paste your code here:", height=200)
    elif input_method == "File Upload":
        uploaded_files = st.file_uploader("Upload project files:", accept_multiple_files=True)

        code_snippet = read_uploaded_files(uploaded_files)
    else:  # Folder Upload
        folder_path = st.text_input("Paste the folder path")

        if folder_path:
            project_files, project_tree = process_folder(folder_path)
            concatenated_content = concatenate_file_contents(project_files)
            # Format the tree structure for better readability
            formatted_tree = textwrap.indent(project_tree, "    ")
            code_snippet = f"""{concatenated_content}

            The tree structure of the project is:\n\n{formatted_tree}
            """

    st.info(
        f"{Emoji.INFO.value} You can paste code from any programming language. The AI will attempt to optimize and improve it based on the given prompt."  # noqa: E501
    )

    # Prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{code_snippet}"),
        ]
    )

    # Generate button
    if st.button(f"{Emoji.ENHANCE_ACTION.value} Enhance Code"):
        with st.spinner(f"{Emoji.AI_RESPONSE.value} Analyzing and optimizing your code..."):
            try:
                llm_response = get_llm_response(st.session_state.llm_config, prompt, {"code_snippet": code_snippet})
                st.session_state.enhancement_history.append(llm_response)

                st.success(f"{Emoji.SUCCESS.value} Code enhancement complete!")
                st.markdown(f"### {Emoji.OPTIMIZATION_RESULT.value} Optimized Code and Suggestions:")
                st.code(llm_response)
            except Exception as e:
                st.error(f"An error occurred during code enhancement: {e}")

    # Previous messages
    with st.expander(f"{Emoji.HISTORY.value} Enhancement History"):
        for i, message in enumerate(st.session_state.enhancement_history):
            st.markdown(f"**{Emoji.ANALYSIS.value} Enhancement {i+1}:**")
            st.code(message)
            st.markdown("---")


def config_tab() -> None:
    def llm_settings() -> None:
        st.subheader(f"{Emoji.AI_MODEL.value} AI Model Settings")
        provider_options = list(PROVIDER_DICT.keys())

        st.selectbox(
            f"{Emoji.AI_PROVIDER.value} AI Provider",
            options=provider_options,
            index=safe_get_index(st.session_state.config.get("llm_provider_index", 0), provider_options),
            help="Choose the AI Provider for code enhancement.",
            key="llm_provider_choose",
            on_change=update_llm_provider,
            args=(provider_options,),
        )

        provider, api_key, models, base_url = PROVIDER_DICT[st.session_state.llm_provider_choose]
        st.session_state.config["llm_provider"] = provider
        st.session_state.config["api_key"] = os.getenv(api_key, "")
        st.session_state.config["base_url"] = base_url

        check_api_key(
            provider_name=provider,
            api_key=api_key,
        )

        st.selectbox(
            f"{Emoji.AI_MODEL.value} AI Model",
            options=models,
            index=safe_get_index(st.session_state.config.get("llm_model_index", 0), models),
            help="Select your AI Model for code optimization.",
            key="llm_model",
            on_change=update_llm_model,
            args=(models,),
        )

        st.slider(
            f"{Emoji.TEMPERATURE.value} Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.config.get("temperature", 0.7),
            step=0.1,
            help="Adjust the creativity of your AI model. Higher values increase output variability.",
            key="temperature",
            on_change=update_config,
            args=("temperature",),
        )

    def advanced_settings() -> None:
        with st.expander(f"{Emoji.ADVANCED_SETTINGS.value} Advanced Settings"):
            st.text_input(
                f"{Emoji.API_KEY.value} API Key",
                type="password",
                value=st.session_state.config.get("api_key", ""),
                help="Enter your API key for the selected AI provider.",
                key="api_key",
                on_change=update_config,
                args=("api_key",),
            )
            st.text_input(
                f"{Emoji.BASE_URL.value} Provider Base URL",
                value=st.session_state.config.get("base_url", ""),
                help="Specify the base URL for the AI provider if required.",
                key="base_url",
                on_change=update_config,
                args=("base_url",),
            )

            st.subheader(f"{Emoji.AI_RESPONSE.value} Response Settings")
            st.number_input(
                f"{Emoji.MAX_TOKENS.value} Max Token Length",
                min_value=1,
                max_value=4096,
                value=st.session_state.config.get("max_tokens", 4096),
                help="Set the maximum length of your AI model's responses.",
                key="max_tokens",
                on_change=update_config,
                args=("max_tokens",),
            )

    def save_reset_buttons() -> None:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"{Emoji.SAVE_CONFIG.value} Save Configuration", key="save_config"):
                update_config_and_session_state(st.session_state.config)
                st.success(f"{Emoji.SUCCESS.value} Your configuration has been saved!")
        with col2:
            if st.button(f"{Emoji.RESET_CONFIG.value} Reset Configuration", key="reset_config"):
                st.session_state.config = Config("default_settings.toml").load()
                update_config_and_session_state(st.session_state.config)
                st.rerun()
        with col3:
            st.checkbox(
                f"{Emoji.AUTO_SAVE.value} Enable Auto-Save",
                value=st.session_state.config.get("autosave_enabled", False),
                key="autosave_enabled",
                on_change=update_config,
                args=("autosave_enabled",),
            )

    def display_current_config() -> None:
        with st.expander(f"{Emoji.CURRENT_CONFIG.value} Current Configuration"):
            st.json(st.session_state.config)

    llm_settings()
    advanced_settings()
    save_reset_buttons()
    display_current_config()


def about_tab() -> None:
    def get_system_info() -> dict[str, str]:
        memory = psutil.virtual_memory()
        return {
            "operating_system": f"{platform.system()} {platform.release()}",
            "processor": platform.processor(),
            "machine": platform.machine(),
            "total_memory": f"{memory.total / (1024**3):.2f} GB",
            "available_memory": f"{memory.available / (1024**3):.2f} GB",
            "cpu_cores": f"{psutil.cpu_count(logical=False)} (Physical), {psutil.cpu_count(logical=True)} (Logical)",
            "cpu_usage": f"{psutil.cpu_percent()}%",
        }

    # Application Info
    st.subheader(f"{Emoji.INFO.value} Application Information")
    col1, col2 = st.columns(2)

    with col1, st.container(border=True):
        st.markdown(f"**{Emoji.NAME.value} Name:** Code Enhancer")
        st.markdown(f"**{Emoji.VERSION.value} Version:** {version}")
        st.markdown(f"**{Emoji.DEVELOPER.value} Developer:** {author_name}")
    with col2, st.container(border=True):
        st.markdown(
            f"""
            **{Emoji.DESCRIPTION.value} Description:** Code Enhancer is an AI-powered tool that helps you analyze, optimize, and transform your code into high-performance, quality software.
            Leverage the power of advanced algorithms to enhance code quality, improve efficiency, and master the art of writing excellent code across various programming languages!
            """  # noqa: E501
        )

    # System Info
    st.subheader(f"{Emoji.OS_INFO.value} System Information")
    system_info = get_system_info()
    col1, col2 = st.columns(2)
    with col1, st.container(border=True):
        st.markdown(f"**{Emoji.OS_INFO.value} Operating System:** {system_info['operating_system']}")
        st.markdown(f"**{Emoji.PROCESSOR_INFO.value} Processor:** {system_info['processor']}")
        st.markdown(f"**{Emoji.OS_INFO.value} Machine:** {system_info['machine']}")
    with col2, st.container(border=True):
        st.markdown(f"**{Emoji.MEMORY_INFO.value} Total Memory:** {system_info['total_memory']}")
        st.markdown(f"**{Emoji.MEMORY_INFO.value} Available Memory:** {system_info['available_memory']}")
        st.markdown(f"**{Emoji.PROCESSOR_INFO.value} CPU Cores:** {system_info['cpu_cores']}")
        st.markdown(f"**{Emoji.PROCESSOR_INFO.value} CPU Usage:** {system_info['cpu_usage']}")

    # Python Environment
    st.subheader(f"{Emoji.PYTHON_INFO.value} Python Environment")
    col1, col2 = st.columns(2)
    with col1, st.container(border=True):
        st.markdown(f"**{Emoji.VERSION.value} Python Version:** {sys.version.split()[0]}")
        st.markdown(f"**{Emoji.PYTHON_INFO.value} Python Implementation:** {platform.python_implementation()}")
    with col2, st.container(border=True):
        st.markdown(f"**{Emoji.VERSION.value} Streamlit Version:** {st.__version__}")
        st.markdown(f"**{Emoji.OS_INFO.value} Working Directory:** {os.path.abspath(os.getcwd())}")

    # Credits and Acknowledgments
    st.subheader(f"{Emoji.CREDITS.value} Acknowledgments")
    with st.container(border=True):
        st.markdown(
            f"""
            <ul>
                <li>
                    {render_image(path="logo/streamlit_logo.png", width="24px")}
                    <a href="https://streamlit.io" target="_blank" rel="noopener noreferrer">Streamlit</a> - The framework used to build this interactive application.
                </li>
                <li>
                    {Emoji.LANGCHAIN.value}
                    <a href="https://www.langchain.com" target="_blank" rel="noopener noreferrer">LangChain</a> - For facilitating the integration of language models into applications.
                </li>
                <li>
                    {Emoji.AI_PROVIDER.value}
                    <strong>Provider Configuration:</strong>
                    <ul>
                        <li><a href="https://github.com/marketplace/models" target="_blank" rel="noopener noreferrer">GitHub Models</a></li>
                        <li><a href="https://aistudio.google.com/" target="_blank" rel="noopener noreferrer">Google GenAI</a></li>
                        <li><a href="https://cohere.com/" target="_blank" rel="noopener noreferrer">Cohere API</a></li>
                        <li><a href="https://groq.com" target="_blank" rel="noopener noreferrer">Groq</a></li>
                        <li><a href="https://www.anthropic.com" target="_blank" rel="noopener noreferrer">Anthropic</a></li>
                        <li><a href="https://www.together.ai" target="_blank" rel="noopener noreferrer">Together AI</a></li>
                        <li><a href="https://ollama.com" target="_blank" rel="noopener noreferrer">Ollama</a></li>
                    </ul>
                </li>
            </ul>
            """,  # noqa: E501
            unsafe_allow_html=True,
        )

    # License Information
    with st.expander(f"{Emoji.LICENSE.value} License"):
        st.markdown(
            f"""
        MIT License

        Copyright (c) 2024 {author_name}

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """
        )


# Helper functions
def update_llm_provider(provider_options: list) -> None:
    llm_provider_choose = st.session_state.llm_provider_choose
    provider, api_key, models, base_url = PROVIDER_DICT[llm_provider_choose]

    st.session_state.config["llm_provider_index"] = provider_options.index(llm_provider_choose)
    st.session_state.config["llm_provider"] = provider
    st.session_state.config["llm_provider_choose"] = llm_provider_choose
    st.session_state.config["llm_model"] = models[safe_get_index(st.session_state.config.get("llm_model_index", 0), models)]
    st.session_state.config["api_key"] = os.getenv(api_key, "")
    st.session_state.config["base_url"] = base_url

    update_config_and_session_state(st.session_state.config)


def update_llm_model(models: list) -> None:
    st.session_state.config["llm_model_index"] = models.index(st.session_state.llm_model)
    st.session_state.config["llm_model"] = st.session_state.llm_model
    update_config_and_session_state(st.session_state.config)


def update_config(key: str) -> None:
    value = st.session_state[key]
    st.session_state.config[key] = value
    update_config_and_session_state(st.session_state.config)


def update_config_and_session_state(new_config: dict) -> None:
    # Update session_state
    for key, value in new_config.items():
        st.session_state.config[key] = value

    # Update configuration file
    config.update(new_config)

    # Ensure LLM configuration is updated
    update_llm_config()


def update_llm_config() -> None:
    st.session_state.llm_config = LLMConfig(
        model=st.session_state.config.get("llm_model", ""),
        model_provider=st.session_state.config.get("llm_provider", ""),
        api_key=st.session_state.config.get("api_key", ""),
        base_url=st.session_state.config.get("base_url", None),
        temperature=st.session_state.config.get("temperature", 0.7),
        max_tokens=st.session_state.config.get("max_tokens", 4096),
        streaming=True,
    )


def safe_get_index(index: int, options: list[Any]) -> int:
    if index < 0 or index >= len(options):
        return 0
    return index


def tabs() -> None:
    st.html(
        f"""
        <h2 style="display:inline;">{render_image("logo/logo.svg")} Code Enhancer: Multi-language Code Optimization</h2>
        """
    )

    st.html(
        f"""
        <p class="big-font">Transform your code into high-performance, quality software! {Emoji.ENHANCE_ACTION.value}</p>
        """
    )

    tab1, tab2, tab3 = st.tabs(
        [
            f"{Emoji.ENHANCE_TAB.value} Enhance",
            f"{Emoji.CONFIGURE_TAB.value} Configure",
            f"{Emoji.ABOUT_TAB.value} About",
        ]
    )

    if "llm_config" not in st.session_state:
        update_llm_config()

    with tab1:
        main_tab()
    with tab2:
        config_tab()
    with tab3:
        about_tab()

    # Footer
    st.markdown("---")
    st.html(
        f"""
        <div style="text-align: center;">
            <p>Made with {Emoji.HEART.value} by {author_name}</p>
            <p>© 2024 Code Enhancer Inc.</p>
        </div>
        """
    )


if __name__ == "__main__":
    tabs()
