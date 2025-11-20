from google.adk.agents import Agent
from devops_automator.tools import file_reader_tool

# Common model configuration
MODEL_NAME = "gemini-2.5-flash-lite"

# 1. AI-Powered Unit Test Generator
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

# 2. Autonomous Debugging Agent
debugging_agent = Agent(
    name="autonomous_debugger",
    model=MODEL_NAME,
    description="Analyzes error logs and source code to identify bugs and propose fixes.",
    instruction="""
    You are a Lead Backend Engineer.
    Your goal is to fix broken code.
    
    1.  The user will provide an error message or describe a bug.
    2.  Use the 'read_code_file' tool to read the file causing the issue.
    3.  Trace the error back to the specific line of code.
    4.  Explain *why* it failed (Root Cause Analysis).
    5.  Provide the corrected code snippet.
    """,
    tools=[file_reader_tool]
)

# 3. Security Vulnerability Scanner Agent
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