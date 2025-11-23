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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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


def aggregate_reports(security_report: str, quality_report: str, test_coverage_notes: str = "") -> str:
    """
    Combines multiple specialist reports into a unified comprehensive audit.
    
    This tool aggregates findings from security, quality, and testing agents
    into a single prioritized report for code reviews and PR audits.
    
    Args:
        security_report: Output from security_scanner agent
        quality_report: Output from code_quality_checker agent  
        test_coverage_notes: Notes about test coverage from unit_test_generator
    
    Returns:
        str: Formatted comprehensive report with prioritized findings and
             overall recommendation (APPROVE / CONDITIONAL / REJECT)
    
    Examples:
        >>> report = aggregate_reports(sec_report, qual_report, test_notes)
        >>> print(report)
        ============================================================
        COMPREHENSIVE CODE AUDIT REPORT
        ...
    """
    import re
    
    # Parse severity from each report
    critical_issues = []
    warnings = []
    suggestions = []
    
    # Extract from security report
    if security_report and ("Critical" in security_report or "High" in security_report or "SQL" in security_report or "injection" in security_report.lower()):
        # Extract critical security issues
        for line in security_report.split('\n'):
            if any(word in line.lower() for word in ['sql injection', 'xss', 'critical', 'high severity']):
                critical_issues.append(f"🔴 SECURITY: {line.strip()}")
                break
        else:
            critical_issues.append("🔴 SECURITY: Critical vulnerabilities detected - see detailed report")
    
    # Extract from quality report
    if quality_report:
        # Check for low scores
        score_match = re.search(r'(\d+\.?\d*)/10', quality_report)
        if score_match:
            score = float(score_match.group(1))
            if score < 5.0:
                critical_issues.append(f"🔴 QUALITY: Very low code quality score ({score}/10)")
            elif score < 7.0:
                warnings.append(f"⚠️ QUALITY: Below-average code quality score ({score}/10)")
        
        # Check for complexity
        if "Grade: F" in quality_report or "Grade F" in quality_report:
            critical_issues.append("🔴 QUALITY: Extremely complex code detected (Grade F)")
        elif "Grade: D" in quality_report or "Grade D" in quality_report:
            warnings.append("⚠️ QUALITY: Very complex code (Grade D) - refactoring recommended")
        elif "Grade: C" in quality_report or "Grade C" in quality_report:
            suggestions.append("💡 QUALITY: Moderate complexity (Grade C) - consider simplification")
    
    # Extract from test coverage
    if test_coverage_notes:
        coverage_match = re.search(r'(\d+)%', test_coverage_notes)
        if coverage_match:
            coverage = int(coverage_match.group(1))
            if coverage < 50:
                critical_issues.append(f"🔴 TESTING: Very low test coverage ({coverage}%)")
            elif coverage < 80:
                warnings.append(f"⚠️ TESTING: Insufficient test coverage ({coverage}%)")
            else:
                suggestions.append(f"✅ TESTING: Good test coverage ({coverage}%)")
    
    # Build unified report
    report = "=" * 70 + "\n"
    report += "           COMPREHENSIVE CODE AUDIT REPORT\n"
    report += "=" * 70 + "\n\n"
    
    # Executive Summary
    report += "EXECUTIVE SUMMARY:\n"
    report += "-" * 70 + "\n"
    
    if critical_issues:
        report += "🚨 CRITICAL ISSUES FOUND - MUST FIX BEFORE MERGE:\n"
        for issue in critical_issues:
            report += f"   {issue}\n"
        report += "\n"
    
    if warnings:
        report += "⚠️  WARNINGS - SHOULD ADDRESS:\n"
        for warn in warnings:
            report += f"   {warn}\n"
        report += "\n"
    
    if suggestions and not critical_issues:
        report += "💡 SUGGESTIONS FOR IMPROVEMENT:\n"
        for sugg in suggestions:
            report += f"   {sugg}\n"
        report += "\n"
    
    if not critical_issues and not warnings:
        report += "✅ No critical issues or warnings detected\n\n"
    
    # Detailed Sections
    report += "=" * 70 + "\n"
    report += "DETAILED ANALYSIS:\n"
    report += "=" * 70 + "\n\n"
    
    report += "━" * 70 + "\n"
    report += "1. SECURITY ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if security_report:
        report += security_report + "\n\n"
    else:
        report += "No security scan results provided.\n\n"
    
    report += "━" * 70 + "\n"
    report += "2. CODE QUALITY ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if quality_report:
        report += quality_report + "\n\n"
    else:
        report += "No quality analysis results provided.\n\n"
    
    report += "━" * 70 + "\n"
    report += "3. TEST COVERAGE ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if test_coverage_notes:
        report += test_coverage_notes + "\n\n"
    else:
        report += "No test coverage analysis provided.\n\n"
    
    # Final Recommendation
    report += "=" * 70 + "\n"
    report += "FINAL RECOMMENDATION:\n"
    report += "=" * 70 + "\n"
    
    if critical_issues:
        report += "❌ REJECT - DO NOT MERGE\n"
        report += "   Critical issues must be resolved before this code can be merged.\n"
        report += f"   Found {len(critical_issues)} critical issue(s) requiring immediate attention.\n"
    elif warnings:
        report += "⚠️  CONDITIONAL APPROVAL\n"
        report += "   Code can be merged after addressing the warnings above.\n"
        report += f"   Found {len(warnings)} warning(s) that should be addressed.\n"
    else:
        report += "✅ APPROVED FOR MERGE\n"
        report += "   Code meets quality standards and security requirements.\n"
        if suggestions:
            report += f"   Consider implementing {len(suggestions)} suggestion(s) for further improvement.\n"
    
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


def aggregate_reports(security_report: str, quality_report: str, test_coverage_notes: str = "") -> str:
    """
    Combines multiple specialist reports into a unified comprehensive audit.
    
    This tool aggregates findings from security, quality, and testing agents
    into a single prioritized report for code reviews and PR audits.
    
    Args:
        security_report: Output from security_scanner agent
        quality_report: Output from code_quality_checker agent  
        test_coverage_notes: Notes about test coverage from unit_test_generator
    
    Returns:
        str: Formatted comprehensive report with prioritized findings and
             overall recommendation (APPROVE / CONDITIONAL / REJECT)
    
    Examples:
        >>> report = aggregate_reports(sec_report, qual_report, test_notes)
        >>> print(report)
        ============================================================
        COMPREHENSIVE CODE AUDIT REPORT
        ...
    """
    import re
    
    # Parse severity from each report
    critical_issues = []
    warnings = []
    suggestions = []
    
    # Extract from security report
    if security_report and ("Critical" in security_report or "High" in security_report or "SQL" in security_report or "injection" in security_report.lower()):
        # Extract critical security issues
        for line in security_report.split('\n'):
            if any(word in line.lower() for word in ['sql injection', 'xss', 'critical', 'high severity']):
                critical_issues.append(f"🔴 SECURITY: {line.strip()}")
                break
        else:
            critical_issues.append("🔴 SECURITY: Critical vulnerabilities detected - see detailed report")
    
    # Extract from quality report
    if quality_report:
        # Check for low scores
        score_match = re.search(r'(\d+\.?\d*)/10', quality_report)
        if score_match:
            score = float(score_match.group(1))
            if score < 5.0:
                critical_issues.append(f"🔴 QUALITY: Very low code quality score ({score}/10)")
            elif score < 7.0:
                warnings.append(f"⚠️ QUALITY: Below-average code quality score ({score}/10)")
        
        # Check for complexity
        if "Grade: F" in quality_report or "Grade F" in quality_report:
            critical_issues.append("🔴 QUALITY: Extremely complex code detected (Grade F)")
        elif "Grade: D" in quality_report or "Grade D" in quality_report:
            warnings.append("⚠️ QUALITY: Very complex code (Grade D) - refactoring recommended")
        elif "Grade: C" in quality_report or "Grade C" in quality_report:
            suggestions.append("💡 QUALITY: Moderate complexity (Grade C) - consider simplification")
    
    # Extract from test coverage
    if test_coverage_notes:
        coverage_match = re.search(r'(\d+)%', test_coverage_notes)
        if coverage_match:
            coverage = int(coverage_match.group(1))
            if coverage < 50:
                critical_issues.append(f"🔴 TESTING: Very low test coverage ({coverage}%)")
            elif coverage < 80:
                warnings.append(f"⚠️ TESTING: Insufficient test coverage ({coverage}%)")
            else:
                suggestions.append(f"✅ TESTING: Good test coverage ({coverage}%)")
    
    # Build unified report
    report = "=" * 70 + "\n"
    report += "           COMPREHENSIVE CODE AUDIT REPORT\n"
    report += "=" * 70 + "\n\n"
    
    # Executive Summary
    report += "EXECUTIVE SUMMARY:\n"
    report += "-" * 70 + "\n"
    
    if critical_issues:
        report += "🚨 CRITICAL ISSUES FOUND - MUST FIX BEFORE MERGE:\n"
        for issue in critical_issues:
            report += f"   {issue}\n"
        report += "\n"
    
    if warnings:
        report += "⚠️  WARNINGS - SHOULD ADDRESS:\n"
        for warn in warnings:
            report += f"   {warn}\n"
        report += "\n"
    
    if suggestions and not critical_issues:
        report += "💡 SUGGESTIONS FOR IMPROVEMENT:\n"
        for sugg in suggestions:
            report += f"   {sugg}\n"
        report += "\n"
    
    if not critical_issues and not warnings:
        report += "✅ No critical issues or warnings detected\n\n"
    
    # Detailed Sections
    report += "=" * 70 + "\n"
    report += "DETAILED ANALYSIS:\n"
    report += "=" * 70 + "\n\n"
    
    report += "━" * 70 + "\n"
    report += "1. SECURITY ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if security_report:
        report += security_report + "\n\n"
    else:
        report += "No security scan results provided.\n\n"
    
    report += "━" * 70 + "\n"
    report += "2. CODE QUALITY ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if quality_report:
        report += quality_report + "\n\n"
    else:
        report += "No quality analysis results provided.\n\n"
    
    report += "━" * 70 + "\n"
    report += "3. TEST COVERAGE ANALYSIS:\n"
    report += "━" * 70 + "\n"
    if test_coverage_notes:
        report += test_coverage_notes + "\n\n"
    else:
        report += "No test coverage analysis provided.\n\n"
    
    # Final Recommendation
    report += "=" * 70 + "\n"
    report += "FINAL RECOMMENDATION:\n"
    report += "=" * 70 + "\n"
    
    if critical_issues:
        report += "❌ REJECT - DO NOT MERGE\n"
        report += "   Critical issues must be resolved before this code can be merged.\n"
        report += f"   Found {len(critical_issues)} critical issue(s) requiring immediate attention.\n"
    elif warnings:
        report += "⚠️  CONDITIONAL APPROVAL\n"
        report += "   Code can be merged after addressing the warnings above.\n"
        report += f"   Found {len(warnings)} warning(s) that should be addressed.\n"
    else:
        report += "✅ APPROVED FOR MERGE\n"
        report += "   Code meets quality standards and security requirements.\n"
        if suggestions:
            report += f"   Consider implementing {len(suggestions)} suggestion(s) for further improvement.\n"
    
    report += "=" * 70 + "\n"
    
    return report


# Wrap aggregate function as ADK tool
aggregate_reports_tool = FunctionTool(func=aggregate_reports)


def write_code_file(file_path: str, content: str) -> str:
    """
    Writes code to a file with safety checks.
    
    This tool enables agents to modify code files with automatic backup
    and path validation for security.
    
    Args:
        file_path: Path to the file to write (relative or absolute)
        content: The new content to write to the file
    
    Returns:
        str: Success message or error description
    
    Security:
        - Validates path is within project directory
        - Creates automatic .backup file before writing
        - Returns detailed status message
    
    Examples:
        >>> result = write_code_file('test.py', 'print("Hello")')
        >>> print(result)
        Successfully wrote 15 characters to test.py (backup created)
    """
    import os
    try:
        # Path validation (same as read_code_file)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        requested_path = os.path.abspath(file_path)
        
        if not requested_path.startswith(base_dir):
            return "Error: Access denied. Can only write within project directory."
        
        # Create backup if file exists
        import shutil
        backup_created = False
        if os.path.exists(requested_path):
            backup_path = requested_path + '.backup'
            shutil.copy2(requested_path, backup_path)
            backup_created = True
        
        # Write the content
        with open(requested_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        backup_msg = " (backup created)" if backup_created else ""
        return f"Successfully wrote {len(content)} characters to {os.path.basename(file_path)}{backup_msg}"
    
    except Exception as e:
        return f"Error writing file: {str(e)}"


def git_revert_file(file_path: str) -> str:
    """
    Reverts a file to its last committed state using git.
    
    This tool provides safe rollback functionality for the refactoring pipeline,
    restoring files to their state in the git repository.
    
    Args:
        file_path: Path to the file to revert (relative or absolute)
    
    Returns:
        str: Success message or error description
    
    Examples:
        >>> result = git_revert_file('vulnerable_app.py')
        >>> print(result)
        Successfully reverted vulnerable_app.py to last commit
    """
    import os
    import subprocess
    try:
        # Path validation
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        requested_path = os.path.abspath(file_path)
        
        if not requested_path.startswith(base_dir):
            return "Error: Access denied. Can only revert files within project directory."
        
        if not os.path.exists(requested_path):
            return f"Error: File not found at {file_path}"
        
        # Run git checkout to revert
        result = subprocess.run(
            ['git', 'checkout', 'HEAD', '--', file_path],
            capture_output=True,
            text=True,
            cwd=base_dir,
            timeout=10
        )
        
        if result.returncode == 0:
            return f"Successfully reverted {os.path.basename(file_path)} to last commit"
        else:
            return f"Error reverting file: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "Error: Git revert timed out"
    except FileNotFoundError:
        return "Error: Git not found. Please ensure git is installed."
    except Exception as e:
        return f"Error reverting file: {str(e)}"


# Wrap new tools as ADK tools
file_writer_tool = FunctionTool(func=write_code_file)
git_revert_tool = FunctionTool(func=git_revert_file)