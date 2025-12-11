# AI Coding Agent (Python + Gemini 2.5)

This project implements a local AI coding agent powered by Google Gemini 2.5 Flash.
The agent can intelligently read, write, and execute files inside your working directory using a structured tool-calling loop.

It supports:
- Listing files and directories
- Reading file contents
- Writing or overwriting files
- Executing Python files with arguments
- Iterative tool call planning
- Automatic prompt + token usage tracking (with --verbose)

## Features
**Tool-Driven Code Execution** >
The model is allowed to call your custom functions:
- get_files_info
- get_file_content
- write_file
- run_python_file

**Iterative Agent Loop** >
The system repeatedly sends all messages (user, assistant, and tool outputs) back to Gemini until:
- the model returns final natural language text, or
- the maximum number of iterations is reached.
This gives the model the ability to:
- Plan multi-step tasks
- Inspect and modify files
- Execute Python and inspect the results
- Continue reasoning based on prior tool output

**Verbose flag:** `--verbose` >
Add the flag to print:
- prompt token count
- response token count
- iteration numbers
- tool call responses

*Example:*
`python main.py "How do I refactor this file?" --verbose`

## Installation
1. Clone the repository
```
git clone https://github.com/wldn-kim/aiagent
cd <project-directory>
```
2. Install dependencies
`pip install -r requirements.txt`

Required packages include:
-google-genai
-python-dotenv

3. Add your Gemini API key

Create a ```.env``` file:

```GEMINI_API_KEY=your_api_key_here```
