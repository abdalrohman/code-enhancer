code_enhancer_prompt = """Your task is to analyze the provided code snippet and suggest improvements to optimize its performance and enhance its overall quality. Follow these guidelines:

1. Performance Optimization:
    - Identify areas where the code can be made more efficient, faster, or less resource-intensive.
    - Provide specific suggestions for optimization, along with explanations of how these changes can enhance the code's performance.
    - Consider time complexity and space complexity in your analysis.

2. Code Quality:
    - Ensure the code follows best practices and style guidelines for the given programming language.
    - Suggest improvements for readability, maintainability, and modularity.
    - Recommend appropriate use of comments and documentation.

3. Idiomatic Practices:
    - Propose changes to make the code more idiomatic for the specific programming language.
    - Suggest the use of language-specific features or built-in functions where appropriate.

4. Error Handling and Edge Cases:
    - Identify potential edge cases or error scenarios that the current code might not handle well.
    - Suggest appropriate error handling and input validation techniques.

5. Design Patterns and Best Practices:
    - Recommend the application of relevant design patterns or best practices that could improve the code structure.
    - Suggest ways to improve code reusability and reduce duplication.

6. Modern Language Features:
    - If applicable, suggest the use of modern language features that could benefit the code.

7. Performance Profiling:
    - If relevant, suggest tools or techniques for profiling the code to identify performance bottlenecks.

Provide your suggestions in a clear, step-by-step manner, explaining the rationale behind each proposed change. The optimized code should maintain the same functionality as the original code while demonstrating improved efficiency and adherence to best practices.

After providing your suggestions, offer a rewritten version of the code that incorporates all the proposed improvements.
"""  # noqa: E501

markdown_writing_prompt = """Write a detailed Github README.md for a new open-source project based on the provided code. The README should follow this structure and include the following sections:

1. Project Title and Description
   - Start with a clear, concise title for the project
   - Provide a brief (2-3 sentences) yet informative description of the project
   - Include any relevant badges (e.g., build status, version, license)

2. Table of Contents
   - Create a clickable table of contents for easy navigation

3. Features
   - List the key features and functionalities of the project
   - Use bullet points for clarity

4. Prerequisites
   - Specify any prerequisites or dependencies required to use the project

5. Installation
   - Provide step-by-step installation instructions
   - Include any necessary commands or code snippets
   - Consider different operating systems if applicable

6. Usage
   - Offer clear examples of how to use the project
   - Include code snippets and explanations
   - Provide sample input/output if relevant

7. Configuration
   - Explain any configuration options or environment variables
   - Provide examples of common configurations

8. API Reference (if applicable)
   - Document the main functions, classes, or methods
   - Include parameters, return types, and brief descriptions

9. Contributing
   - Outline well-defined contribution guidelines
   - Explain the process for submitting pull requests
   - Include any coding standards or conventions to follow

10. Testing
    - Describe how to run the test suite
    - Explain how to write and add new tests

11. Deployment (if applicable)
    - Provide instructions for deploying the project

12. Built With
    - List the main technologies, frameworks, or libraries used

13. Versioning
    - Explain the versioning scheme used (e.g., Semantic Versioning)

14. Authors
    - Credit the main contributors to the project

15. License
    - Specify the license under which the project is released
    - Include a link to the full license text

16. Acknowledgments
    - Thank any individuals or projects that inspired or helped this project

17. FAQ (optional)
    - Address common questions or issues users might encounter

Remember to use appropriate Markdown formatting throughout the README, including headers, code blocks, links, and emphasis where needed. Aim for a professional yet friendly tone, and ensure the content is clear and easy to understand for both beginners and experienced developers.
"""  # noqa: E501
