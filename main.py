import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) == 1:
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    verbose = False
    print("No prompt provided — using default: Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
else:
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)
client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

def main():
    max_iterations = 20

    for i in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            if "--verbose" in sys.argv:
                print(f"Iteration {i + 1}:")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
            
            if response.function_calls:
                for function_call in response.function_calls:
                    function_result = call_function(function_call, verbose=verbose)

                    if not function_result.parts or not hasattr(function_result.parts[0], "function_response"):
                        raise RuntimeError("Fatal error: Missing function response from call_function.")
                    if verbose:
                        print("->", function_result.parts[0].function_response.response)
                    
                    tool_message = types.Content(
                        role="tool",
                        parts=function_result.parts
                    )
                    messages.append(tool_message)
                continue

            if response.text:
                print(response.text)
                break
        except Exception as e:
            print(f"Error during generate_content loop: {e}")
            break
    else:
        print("Max iterations reached without final response.")

if __name__ == "__main__":
    main()
