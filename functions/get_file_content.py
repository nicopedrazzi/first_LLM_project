import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.join(abs_path,file_path)
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if valid_target_dir is False:
            return  f'Error: Cannot read "{target_dir}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir) is not True:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir,"r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'



schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a specified file in file_path up to 10000 characters. If more the content will be truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content from.",
            ),
        },
    ),
)
