import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    full_dir = os.path.join(working_directory, directory)

    if not os.path.abspath(full_dir).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    
    if not os.path.isdir(full_dir):
        return f"Error: '{directory}' is not a directory"
    
    try:
        items = os.listdir(full_dir)
        info_list = []

        for item in items:
            item_path = os.path.join(full_dir, item)
            size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            info_list.append(f"- {item}: file_size={size} bytes, is_dir={is_directory}")

        return "\n".join(info_list)
    
    except Exception as e:
        error_message = str(e)
        return f"Error: {error_message}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)    
    
    