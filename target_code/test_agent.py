import unittest
from unittest.mock import MagicMock, patch

# Mock the ADK Agent class and the sub-agents that root_agent depends on.
# We need to mock the Agent class itself to control its instantiation and behavior,
# and also the specific sub-agent objects that are imported.

# Mock the base Agent class from the ADK framework.
# This is necessary because root_agent inherits from it, and the framework's dispatch logic
# likely resides within the base class's methods (e.g., 'handle').
try:
    from google.adk.agents.llm_agent import Agent
except ImportError:
    # If google.adk is not available, create a mock Agent class for testing purposes.
    class Agent:
        def __init__(self, name, model, description, instruction, sub_agents=None, **kwargs):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction
            self.sub_agents = sub_agents if sub_agents else []
            self._kwargs = kwargs

        def handle(self, request, *args, **kwargs):
            # This is a placeholder for the framework's dispatch logic.
            # In the test, we will override this with a side_effect.
            raise NotImplementedError("Base Agent.handle should be mocked or implemented by framework.")

# Mock the specific sub-agent objects that are imported in agent.py
mock_unit_test_agent = MagicMock()
mock_debugging_agent = MagicMock()
mock_security_agent = MagicMock()

# Patch the imported sub-agents within the module where root_agent is defined (agent.py).
# This ensures that when agent.py is imported for the test, it uses our mocks.
# The patch targets the scope where these names are defined in the 'agent' module.
@patch('devops_automator.agent.unit_test_agent', new=mock_unit_test_agent)
@patch('devops_automator.agent.debugging_agent', new=mock_debugging_agent)
@patch('devops_automator.agent.security_agent', new=mock_security_agent)
class TestDevOpsLeadAgent(unittest.TestCase):

    def setUp(self):
        """Set up mocks and patch the base Agent's handle method before each test."""
        # Reset mocks before each test to ensure isolation
        mock_unit_test_agent.reset_mock()
        mock_debugging_agent.reset_mock()
        mock_security_agent.reset_mock()

        # Patch the 'handle' method of the base Agent class.
        # This mock simulates the ADK framework's routing logic that would be applied to root_agent.
        self.mock_agent_handle = patch.object(Agent, 'handle')
        self.mock_agent_handle_instance = self.mock_agent_handle.start()

        # Define the side effect for the mocked handle method.
        # This function simulates the ADK framework's routing logic based on root_agent's instructions.
        def side_effect_for_handle(request, *args, **kwargs):
            # Check for keywords in the request to determine the intended agent.
            # These keywords are derived from the root_agent's 'instruction' field.
            if "test" in request.lower() and "generate" in request.lower():
                # If generating tests, call the unit_test_agent's invoke method.
                return mock_unit_test_agent.invoke(request, *args, **kwargs)
            elif "bug" in request.lower() or "error" in request.lower():
                # If reporting bugs or errors, call the debugging_agent's invoke method.
                return mock_debugging_agent.invoke(request, *args, **kwargs)
            elif "security" in request.lower() or "scan" in request.lower() or "audit" in request.lower():
                # If requesting security scan or audit, call the security_agent's invoke method.
                return mock_security_agent.invoke(request, *args, **kwargs)
            else:
                # For unhandled requests, return a default message indicating no specific agent was matched.
                return "Default handling: Unrecognized request."

        self.mock_agent_handle_instance.side_effect = side_effect_for_handle

        # Now, get the root_agent instance.
        # We need to import it in a way that uses the patched sub-agents.
        # The module-level @patch decorators should ensure this when 'agent' module is imported.
        import agent # Import the module containing root_agent
        self.root_agent = agent.root_agent

    def tearDown(self):
        """Stop the patch after each test to clean up."""
        self.mock_agent_handle.stop()

    def test_route_to_unit_test_generator(self):
        """
        Test that requests related to generating tests are routed to unit_test_agent.
        """
        user_request = "Generate unit tests for the code."
        
        # Call the handle method on the root_agent instance, simulating the ADK framework's interaction.
        # This call will trigger our mocked Agent.handle's side effect.
        self.root_agent.handle(user_request)
        
        # Assert that the correct sub-agent's invoke method was called exactly once with the user's request.
        mock_unit_test_agent.invoke.assert_called_once_with(user_request)
        # Assert that other sub-agents were not called.
        mock_debugging_agent.invoke.assert_not_called()
        mock_security_agent.invoke.assert_not_called()

    def test_route_to_autonomous_debugger(self):
        """
        Test that requests related to bugs or errors are routed to autonomous_debugger.
        """
        user_request = "I found a bug in the application."
        
        self.root_agent.handle(user_request)
        
        # Assert that the debugging_agent was called.
        mock_debugging_agent.invoke.assert_called_once_with(user_request)
        # Assert that other sub-agents were not called.
        mock_unit_test_agent.invoke.assert_not_called()
        mock_security_agent.invoke.assert_not_called()

    def test_route_to_security_scanner(self):
        """
        Test that requests related to security scans are routed to security_scanner.
        """
        user_request = "Please perform a security audit on the codebase."
        
        self.root_agent.handle(user_request)
        
        # Assert that the security_agent was called.
        mock_security_agent.invoke.assert_called_once_with(user_request)
        # Assert that other sub-agents were not called.
        mock_unit_test_agent.invoke.assert_not_called()
        mock_debugging_agent.invoke.assert_not_called()

    def test_unhandled_request_routing(self):
        """
        Test that requests that don't match any routing rule are handled appropriately.
        """
        user_request = "What is the current time?" # An unhandled request
        
        # Call the handle method and capture the result returned by our side_effect.
        result = self.root_agent.handle(user_request)
        
        # Assert that no sub-agent was invoked for this unhandled request.
        mock_unit_test_agent.invoke.assert_not_called()
        mock_debugging_agent.invoke.assert_not_called()
        mock_security_agent.invoke.assert_not_called()
        
        # Assert that the unhandled request was processed and returned the expected default message.
        self.assertIn("Default handling: Unrecognized request.", result)

if __name__ == '__main__':
    # The unittest.main() function discovers and runs the tests.
    # argv and exit=False are used to help with compatibility in different execution environments.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)