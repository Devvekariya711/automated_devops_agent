import os
from google.adk.tools import FunctionTool

def read_code_file(file_path: str) -> str:
    """
    Reads the content of a code file from the local file system.
    
    This tool provides secure file reading capabilities for AI agents, with
    automatic path validation to prevent directory traversal attacks.
    
    Args:
        file_path: The relative or absolute path to the file to read.
                  Examples: 
                  - 'target_code/vulnerable_app.py'
                  - 'devops_automator/agent.py'
        
    Returns:
        str: The complete content of the file if successful, or a descriptive
             error message if the file cannot be read.
    
    Security:
        - Prevents access to files outside the project directory
        - Blocks path traversal attempts (../ patterns)
        - Validates all paths against the project root
    
    Examples:
        >>> content = read_code_file('target_code/vulnerable_app.py')
        >>> if 'Error' not in content:
        ...     print("File read successfully")
    """

    try:
        # Convert to absolute path and validate it's within project
        base_dir = os.path.abspath(os.path.dirname(__file__))
        requested_path = os.path.abspath(file_path)
        
        # Check if the path is within the project directory
        if not requested_path.startswith(base_dir):
            return "Error: Access denied. You can only read files within the project directory."
        
        if not os.path.exists(requested_path):
            return f"Error: File not found at {file_path}. Please check the path."
        
        with open(requested_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Wrap the python function into an ADK Tool
file_reader_tool = FunctionTool(func=read_code_file)