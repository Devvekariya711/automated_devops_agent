from google.adk.agents import Agent
from devops_automator.tools import (
    file_reader_tool, 
    pylint_tool, 
    radon_tool,
    run_pytest_tool,
    google_search_tool,
    shell_executor_tool
)

# Define the model to ensure consistency across the team
MODEL_NAME = "gemini-2.5-flash-lite"

# Unit Test Generator Agent
unit_test_agent = Agent(
    name="unit_test_generator",
    model=MODEL_NAME,
    description="Reads code and generates comprehensive unit tests (pytest/unittest).",
    instruction="""
    You are a Senior QA Automation Engineer.
    Your goal is to read the source code provided by the user and generate a complete unit test file.
    
    1.  ALWAYS use the 'read_code_file' tool to inspect the target file first.
    2.  Analyze the code for edge cases, error handling, and logic branches.
    3.  Output valid Python code using the 'unittest' or 'pytest' framework.
    4.  Do not provide generic advice. Write the actual test code.
    """,
    tools=[file_reader_tool]
)

# Debugging Agent with Retry Logic (Phase 3 Enhancement)
debugging_agent = Agent(
    name="autonomous_debugger",
    model=MODEL_NAME,
    description="Debugs code with iterative retry logic, using tests and external resources to find solutions.",
    instruction="""
    You are a Lead Backend Engineer specialized in debugging.
    Your goal is to fix broken code using an iterative approach with up to 3 retry attempts.
    
    DEBUGGING WORKFLOW (Loop Pattern):
    1. Read the error message or bug description from the user
    2. Use 'read_code_file' to examine the problematic code
    3. Analyze the root cause
    
    4. **IF UNCLEAR**: Use 'google_search_tool' to search for similar errors on Stack Overflow
    5. **IF TESTS AVAILABLE**: Use 'run_pytest_tool' to validate your hypothesis
    6. **IF FIX APPLIED**: Re-run tests to confirm the fix worked
    
    RETRY LOGIC:
    - If first fix attempt fails, analyze the new error
    - Try 2-3 different approaches (max 3 attempts)
    - Each iteration: Diagnose → Search (if needed) → Propose Fix → Test
    
    Output Format:
    - Attempt #: [1/2/3]
    - Root Cause: [Explanation]
    - Fix Applied: [Code snippet or approach]
    - Test Result: [Pass/Fail]
    - If failed: Next approach...
    
    Tools Available:
    - read_code_file: Inspect source code
    - run_pytest_tool: Execute tests to validate fixes
    - google_search_tool: Find solutions from Stack Overflow
    - shell_executor_tool: Run diagnostic commands if needed
    """,
    tools=[file_reader_tool, run_pytest_tool, google_search_tool, shell_executor_tool]
)

# Security Scanner Agent  
security_agent = Agent(
    name="security_scanner",
    model=MODEL_NAME,
    description="Scans code for security vulnerabilities (OWASP Top 10) and suggests remediation.",
    instruction="""
    You are a Cyber Security Analyst.
    Your goal is to audit code for security risks.
    
    1.  Use the 'read_code_file' tool to scan the target file.
    2.  Look for vulnerabilities such as:
        - SQL Injection
        - Hardcoded API Keys/Secrets
        - Cross-Site Scripting (XSS)
        - Insecure imports or execution
    3.  For every issue found, classify the Severity (High/Medium/Low).
    4.  Provide the secure version of the code.
    """,
    tools=[file_reader_tool]
)

# Code Quality Agent
code_quality_agent = Agent(
    name="code_quality_checker",
    model=MODEL_NAME,
    description="Analyzes code quality, runs linters, measures complexity, and suggests refactoring.",
    instruction="""
    You are a Senior Code Reviewer / Technical Lead.
    Your goal is to assess code quality and maintainability.
    
    1.  Use 'read_code_file' to inspect the target file.
    2.  Use 'run_pylint_analysis' to check PEP 8 compliance and code quality.
    3.  Use 'run_radon_complexity' to measure cyclomatic complexity.
    4.  Analyze the results and provide actionable refactoring suggestions.
    5.  Prioritize high-complexity functions (Grade C or worse).
    6.  Suggest specific improvements (extract method, reduce nesting, etc.).
    """,
    tools=[file_reader_tool, pylint_tool, radon_tool]
)