import os
from google.adk.tools import FunctionTool

def read_code_file(file_path: str) -> str:
    """
    Reads the content of a code file from the local file system.
    
    Args:
        file_path: The relative path to the file (e.g., 'target_code/vulnerable_app.py').
        
    Returns:
        str: The content of the file, or an error message if the file does not exist.
    """
    try:
        # Security check: Prevent reading files outside the project directory
        if ".." in file_path or file_path.startswith("/"):
            return "Error: Access denied. You can only read files within the project directory."

        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}. Please check the path."
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
            
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Wrap the python function into an ADK Tool
file_reader_tool = FunctionTool(func=read_code_file)