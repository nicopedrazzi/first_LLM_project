import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if valid_target_dir is False:
            return  f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) is not True:
            return f'Error: "{directory}" is not a directory'
        x = ""      
        documents_in_folder = os.listdir(target_dir)
        
        for file in documents_in_folder:
            name = str(file)
            filepath = os.path.join(target_dir,name)
            is_dir = os.path.isdir(filepath)
            dimension = os.path.getsize(filepath)

            x = x + f"- {name}: file_size={dimension} bytes, is_dir={is_dir}\n"
        return x
    except Exception as e:
        return f"Error listing files: {e}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

    
