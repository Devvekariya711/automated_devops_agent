import os
import subprocess
import io
from contextlib import redirect_stdout
from google.adk.tools import FunctionTool
from pylint import lint
from pylint.reporters.text import TextReporter
from radon.complexity import cc_visit


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


def run_pylint_analysis(file_path: str) -> str:
    """
    Runs pylint static code analysis on a Python file.
    
    This tool executes pylint to check for PEP 8 compliance, code quality issues,
    and potential bugs. It provides a comprehensive quality score and detailed
    issue list.
    
    Args:
        file_path: The relative or absolute path to the Python file to analyze.
                  Examples: 'vulnerable_app.py', 'devops_automator/agent.py'
    
    Returns:
        str: A formatted report containing:
             - Overall pylint score (0-10)
             - List of issues categorized by type (Convention, Refactor, Warning, Error)
             - Line numbers and descriptions for each issue
             - Or an error message if analysis fails
    
    Examples:
        >>> report = run_pylint_analysis('vulnerable_app.py')
        >>> print(report)
        Pylint Analysis for vulnerable_app.py:
        Overall Score: 6.5/10
        ...
    """
    try:
        # Validate path exists
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}. Please check the path."
        
        # Validate it's a Python file
        if not file_path.endswith('.py'):
            return f"Error: {file_path} is not a Python file. Pylint only works with .py files."
        
        # Run pylint and capture output
        output_buffer = io.StringIO()
        reporter = TextReporter(output_buffer)
        
        # Run pylint with minimal configuration
        pylint_opts = [
            file_path,
            '--reports=y',
            '--score=y'
        ]
        
        # pylint returns non-zero exit codes for issues, which is expected
        try:
            lint.Run(pylint_opts, reporter=reporter, exit=False)
        except SystemExit:
            pass  # pylint calls sys.exit, we catch it
        
        # Get the output
        result = output_buffer.getvalue()
        
        # Format the output more clearly
        if result:
            formatted = f"Pylint Analysis for {os.path.basename(file_path)}:\n"
            formatted += "=" * 60 + "\n"
            formatted += result
            return formatted
        else:
            return f"Pylint ran successfully on {file_path} but produced no output."
            
    except ImportError:
        return "Error: pylint is not installed. Run: pip install pylint>=3.0.0"
    except Exception as e:
        return f"Error running pylint: {str(e)}"


def run_radon_complexity(file_path: str) -> str:
    """
    Analyzes the cyclomatic complexity of functions in a Python file.
    
    This tool uses radon to measure code complexity, helping identify
    functions that are too complex and may need refactoring. Lower
    complexity scores indicate simpler, more maintainable code.
    
    Args:
        file_path: The relative or absolute path to the Python file to analyze.
                  Examples: 'vulnerable_app.py', 'devops_automator/tools.py'
    
    Returns:
        str: A formatted report containing:
             - Complexity grade (A-F) for each function
             - Numeric complexity score
             - Function names and line numbers
             - Recommendations for refactoring
             - Or an error message if analysis fails
    
    Complexity Grades:
        A: 1-5 (Simple, low risk)
        B: 6-10 (Moderate complexity)
        C: 11-20 (Complex, consider refactoring)
        D: 21-30 (Very complex, should refactor)
        F: 31+ (Extremely complex, high risk)
    
    Examples:
        >>> report = run_radon_complexity('vulnerable_app.py')
        >>> print(report)
        Complexity Analysis for vulnerable_app.py:
        Function 'get_user_data' (Line 22): Grade B - Complexity 7
        ...
    """
    try:
        # Validate path exists
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}. Please check the path."
        
        # Validate it's a Python file
        if not file_path.endswith('.py'):
            return f"Error: {file_path} is not a Python file. Radon only works with .py files."
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Analyze complexity
        complexity_results = cc_visit(code_content)
        
        # Format the output
        formatted = f"Complexity Analysis for {os.path.basename(file_path)}:\n"
        formatted += "=" * 60 + "\n"
        
        if not complexity_results:
            formatted += "No functions found or file is too simple to analyze.\n"
            return formatted
        
        # Sort by complexity (highest first)
        complexity_results.sort(key=lambda x: x.complexity, reverse=True)
        
        for item in complexity_results:
            grade = item.letter
            complexity = item.complexity
            name = item.name
            lineno = item.lineno
            
            # Add color-coded interpretation
            if grade in ['A', 'B']:
                status = "✓ Good"
            elif grade == 'C':
                status = "⚠ Consider refactoring"
            else:
                status = "❌ Should refactor"
            
            formatted += f"\nFunction '{name}' (Line {lineno}):\n"
            formatted += f"  Grade: {grade} | Complexity: {complexity} | {status}\n"
        
        # Add summary
        formatted += "\n" + "=" * 60 + "\n"
        formatted += "Complexity Guide:\n"
        formatted += "  A (1-5):   Simple, low risk\n"
        formatted += "  B (6-10):  Moderate complexity\n"
        formatted += "  C (11-20): Complex, consider refactoring\n"
        formatted += "  D (21-30): Very complex, should refactor\n"
        formatted += "  F (31+):   Extremely complex, high risk\n"
        
        return formatted
            
    except ImportError:
        return "Error: radon is not installed. Run: pip install radon>=6.0.0"
    except Exception as e:
        return f"Error running radon complexity analysis: {str(e)}"


# Wrap the python functions into ADK Tools
file_reader_tool = FunctionTool(func=read_code_file)
pylint_tool = FunctionTool(func=run_pylint_analysis)
radon_tool = FunctionTool(func=run_radon_complexity)