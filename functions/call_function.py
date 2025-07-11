import os
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

FUNCTION_REGISTRY = {
    "write_file": write_file,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})

    function_args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_call = FUNCTION_REGISTRY.get(function_name)

    if function_to_call is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    try:
        function_result = function_to_call(**function_args)
    except Exception as e:
        function_result = f"Error while calling function: {e}"
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
