import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)

        merged = os.path.join(working_directory, file_path)
        merged_abs = os.path.abspath(merged)

        if os.path.commonpath([abs_path, merged_abs]) != abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(merged_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", merged_abs]
        if args:
            command.extend(args)

        process_run = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []
        stdout = process_run.stdout or ""
        stderr = process_run.stderr or ""

        if process_run.returncode != 0:
            output_parts.append(f"Process exited with code {process_run.returncode}")

        if stdout.strip():
            output_parts.append(f"STDOUT:\n{stdout.rstrip()}")
        if stderr.strip():
            output_parts.append(f"STDERR:\n{stderr.rstrip()}")

        if not output_parts:
            return "No output produced"

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="If the file extension is '.py' the file gets executed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "the file path of the python file to subprocess.run module, base are be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="other arguments to be added to the subprocess.run function.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
