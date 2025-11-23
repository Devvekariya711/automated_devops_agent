from google.adk.agents.llm_agent import Agent
from devops_automator.supporting_agents import (
    unit_test_agent, 
    debugging_agent, 
    security_agent,
    code_quality_agent
)

# Define the model to ensure consistency across the team
MODEL_NAME = "gemini-2.5-flash-lite"

root_agent = Agent(
    name="devops_lead",
    model=MODEL_NAME,
    description="The main orchestrator that manages testing, debugging, and security tasks.",
    instruction="""
    You are the DevOps Team Lead. You manage a team of specialized AI agents.
    You communicate directly with the user.

    Your Routing Logic:
    1. If the user wants to generate tests -> Delegate to 'unit_test_generator'.
    2. If the user reports a bug or error -> Delegate to 'autonomous_debugger'.
    3. If the user asks for a security scan or audit -> Delegate to 'security_scanner'.
    4. If the user asks to check code quality, refactor, analyze complexity, or check maintainability -> Delegate to 'code_quality_checker'.

    Important Rules:
    - You do not read files yourself. Delegate that to your specialists.
    - If the user has not provided a specific file path (e.g., 'target_code/app.py'), ask them for it before delegating.
    - Always summarize the result returned by your specialists clearly to the user.
    """,
    # This is the key step: We register the specialists as sub-agents.
    # The ADK handles the routing automatically based on the description and instructions.
    sub_agents=[unit_test_agent, debugging_agent, security_agent, code_quality_agent]
)
