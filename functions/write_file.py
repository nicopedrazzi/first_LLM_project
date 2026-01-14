import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.join(working_directory, file_path)
        abs_target = os.path.abspath(target_dir)

        is_correct = os.path.commonpath([abs_path,abs_target]) == abs_path
        if is_correct == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(abs_target)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'



schema_write = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content onto a file located at file_path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to be written on.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="The content to be written on the file located at file_path.",
            ),
        },
    ),
)
