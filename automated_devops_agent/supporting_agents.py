from google.adk.agents import Agent
from automated_devops_agent.tools import (
    file_reader_tool, 
    pylint_tool, 
    radon_tool,
    run_pytest_tool,
    google_search_tool,
    shell_executor_tool
)
from automated_devops_agent.tools import read_memory_tool, update_memory_tool

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
    3.  Generate a complete test file with pytest or unittest syntax.
    4.  Include test cases for happy paths, edge cases, and error handling.
    5.  Return the complete test code in a code block.
    
    Important: Provide clear test descriptions and assert statements.
    """,
    tools=[file_reader_tool]
)

# Debugging Agent  
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
    - Each iteration: Diagnose -> Search (if needed) -> Propose Fix -> Test
    
    IMPORTANT: Always return a clear summary of your findings to the delegating agent.
    
    Output Format:
    - Attempt #: [1/2/3]
    - Root Cause: [Explanation]
    - Fix Applied: [Code snippet or approach]
    - Test Result: [Pass/Fail]
    
    Tools: read_code_file, run_pytest_tool, google_search_tool, shell_executor_tool
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
    
    WORKFLOW:
    1. Use 'read_code_file' to scan the target file
    2. Identify vulnerabilities:
       - SQL Injection
       - Hardcoded API Keys/Secrets
       - Cross-Site Scripting (XSS)
       - Insecure imports or execution
    3. For every issue found, classify Severity (Critical/High/Medium/Low)
    4. Provide secure code examples
    
    CRITICAL: You MUST return your security analysis as a formatted report to the delegating agent.
    
    RESPONSE FORMAT (REQUIRED):
    Security Scan Results for [filename]:
    ========================================
    
    CRITICAL VULNERABILITIES:
    1. [Vulnerability Type] at line [X]: [Description]
       Severity: Critical
       Fix: [Code example]
    
    RECOMMENDATIONS:
    - [Actionable recommendation 1]
    - [Actionable recommendation 2]
    
    Always end with a clear summary of findings.
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
    
    WORKFLOW:
    1. Use 'read_code_file' to inspect the target file
    2. Use 'run_pylint_analysis' to check PEP 8 compliance
    3. Use 'run_radon_complexity' to measure cyclomatic complexity
    4. Synthesize findings into quality report
    
    CRITICAL: You MUST return your quality analysis as a formatted report to the delegating agent.
    
    RESPONSE FORMAT (REQUIRED):
    Code Quality Report for [filename]:
    ====================================
    
    PYLINT SCORE: X.X/10
    
    COMPLEXITY ANALYSIS:
    - Function '[name]': Grade [A-F], Complexity [N]
    
    KEY ISSUES:
    1. [Issue description]
    2. [Issue description]
    
    RECOMMENDATIONS:
    - [Specific actionable improvement]
    - [Specific actionable improvement]
    
    SUMMARY: [Overall assessment in 1-2 sentences]
    
    Always provide this complete report - the root agent needs it for comprehensive audits.
    """,
    tools=[file_reader_tool, pylint_tool, radon_tool]
)
