import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
        if not os.path.isfile(abs_full_path):
            return f"Error: File not found or is not a regular file: '{file_path}'"
        
        MAX_CHARS = 10000
        with open(abs_full_path, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS + 1)

        if len(file_content_string) > MAX_CHARS:
            return file_content_string[:MAX_CHARS] + f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
        
        return file_content_string
    
    except Exception as e:
        error_message = str(e)
        return f"Error: {error_message}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory."
            ),
        },
        required=["file_path"]
    )
)