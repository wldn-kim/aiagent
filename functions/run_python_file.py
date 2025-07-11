import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        cmd = ['python', full_path]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_directory,
            timeout=30,
            text=True
        )

        output_parts = []
        if result.stdout.strip():
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        if not output_parts:
            return "No output produced."

        return "\n\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file within the working directory, optionally with command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python (.py) file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file."
            )
        },
        required=["file_path"]
    )
)