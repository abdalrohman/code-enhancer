## Code Enhancer: Multi-language Code Optimization

**A powerful AI-powered tool to analyze, optimize, and transform your code into high-performance, quality software.**

[![GitHub stars](https://img.shields.io/github/stars/abdalrohman/code-enhancer?style=social)](https://github.com/abdalrohman/code-enhancer)
[![GitHub forks](https://img.shields.io/github/forks/abdalrohman/code-enhancer?style=social)](https://github.com/abdalrohman/code-enhancer)
[![GitHub license](https://img.shields.io/github/license/abdalrohman/code-enhancer)](https://github.com/abdalrohman/code-enhancer/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/abdalrohman/code-enhancer)](https://github.com/abdalrohman/code-enhancer)

## Table of Contents

- [Code Enhancer: Multi-language Code Optimization](#code-enhancer-multi-language-code-optimization)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Built With](#built-with)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [FAQ](#faq)

## Features

- **Multi-language Support:** Optimize code written in various programming languages.
- **AI-Powered Enhancement:** Leverage advanced language models to analyze and suggest improvements.
- **Customizable Prompts:** Tailor the optimization process with specific instructions.
- **Configuration Options:** Choose your preferred AI provider, model, and settings.
- **User-Friendly Interface:**  Intuitive Streamlit interface for easy interaction.
- **Enhancement History:** Keep track of previous optimizations for reference.

## Prerequisites

- **Python 3.10 or later:** Download and install from [https://www.python.org/](https://www.python.org/)
- **pip:** Python package installer (usually included with Python)
- **Streamlit:**  Install using `pip install streamlit`
- **LangChain:**  Install using `pip install langchain`
- **psutil:**  Install using `pip install psutil`
- **dotenv:** Install using `pip install python-dotenv`
- **API Key:** Obtain an API key from your chosen AI provider (e.g., OpenAI, Google GenAI, Cohere).

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdalrohman/code-enhancer.git
   cd code-enhancer
   ```

2. **Create a `.env` file:**
   - Copy the `.env.example` file to `.env`.
   - Fill in your API keys for the desired AI providers.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Select your AI provider and model:**
   - Go to the "Configure" tab.
   - Choose your preferred provider from the dropdown list.
   - Select the desired AI model.

3. **Paste your code:**
   - Go to the "Enhance" tab.
   - Paste your code into the text area.

4. **Customize the optimization prompt (optional):**
   - Expand the "Optimization Prompt" section.
   - Modify the prompt to provide specific instructions for the AI.

5. **Click "Enhance Code":**
   - The application will analyze your code and provide optimized suggestions.

6. **View the results:**
   - The optimized code and suggestions will be displayed.
   - You can access previous enhancement history in the "Enhancement History" section.

## Configuration

- **AI Provider:** Choose from supported providers like OpenAI, Google GenAI, Cohere, and more.
- **AI Model:** Select the specific language model for optimization.
- **Temperature:**  Adjust the creativity and variability of the AI's responses.
- **Max Token Length:**  Set the maximum length of the AI's responses.
- **API Key:**  Enter your API key for the chosen AI provider.
- **Provider Base URL:**  Specify the base URL for the AI provider if required.
- **Autosave:**  Enable automatic saving of your configuration changes.

## Contributing

We welcome contributions to Code Enhancer!

1. **Fork the repository:** Create a fork of the project on GitHub.
2. **Create a branch:** Create a new branch for your feature or bug fix.
3. **Make changes:** Implement your changes and ensure they follow the existing code style.
4. **Submit a pull request:** Submit a pull request to the main branch of the original repository.
5. **Address feedback:** Respond to any feedback or suggestions from the maintainers.


## Built With

- **Streamlit:** Web framework for building interactive applications.
- **LangChain:** Framework for integrating language models into applications.
- **psutil:**  Library for system and process monitoring.
- **dotenv:**  Library for loading environment variables from a `.env` file.


## Authors

- **M.Abdulrahman Alnaseer:** [https://www.github.com/abdalrohman](https://www.github.com/abdalrohman)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Streamlit:**  For providing a powerful and user-friendly framework for building interactive applications.
- **LangChain:**  For simplifying the integration of language models into applications.
- **OpenAI, Google GenAI, Cohere:**  For providing access to their powerful AI models.
- **All contributors:**  For their valuable contributions to this project.

## FAQ

- **Q: What AI providers are supported?**
   - A: Code Enhancer supports a wide range of AI providers, including OpenAI, Google GenAI, Cohere, Anthropic, Together AI, and more.

- **Q: How do I get an API key?**
   - A:  Visit the website of your chosen AI provider and follow their instructions for obtaining an API key.

- **Q: Can I use Code Enhancer for commercial purposes?**
   - A: Yes, Code Enhancer is open source and free to use for both personal and commercial purposes. However, you may need to comply with the terms of service of your chosen AI provider.

- **Q: How do I report a bug or suggest a feature?**
   - A: Please open an issue on the GitHub repository.