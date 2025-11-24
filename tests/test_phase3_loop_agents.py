"""
Integration tests for Phase 3: Loop Agents (Iterative Testing)

Tests the IterativeDebugger functionality including:
- Retry loop with maximum attempts
- Attempt tracking and history logging
- Test execution integration
- Search tool integration when stuck
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from devops_automator.pipelines import IterativeDebugger


class TestLoopAgents(unittest.TestCase):
    """Test suite for Phase 3: Loop Agents."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_file = Path(__file__).parent / "fixtures" / "flaky_code.py"
        self.code_file = Path(__file__).parent / "fixtures" / "flaky_code.py"
    
    def test_debugger_initialization(self):
        """Test that IterativeDebugger initializes correctly."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file),
            max_retries=3
        )
        
        self.assertEqual(debugger.max_retries, 3)
        self.assertEqual(len(debugger.attempts), 0)
        self.assertEqual(debugger.test_file.name, "flaky_code.py")
        
        print("✅ Debugger initialization test passed")
    
    def test_max_retries_default(self):
        """Test that default max_retries is 5."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file)
        )
        
        self.assertEqual(debugger.max_retries, 5)
        
        print("✅ Default max retries test passed")
    
    def test_attempt_tracking(self):
        """Test that attempts are tracked correctly."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file),
            max_retries=2
        )
        
        # Mock the test run to always fail
        with patch.object(debugger, '_run_tests') as mock_run_tests:
            mock_run_tests.return_value = {
                "success": False,
                "output": "FAILED: AssertionError",
                "test_file": str(self.test_file)
            }
            
            # Execute debugging (will reach max retries)
            result = debugger.debug_until_fixed()
            
            # Verify attempts were tracked
            self.assertEqual(len(debugger.attempts), 2)
            self.assertEqual(result["attempts_count"], 2)
            self.assertEqual(result["status"], "max_retries")
            
            # Verify each attempt has required fields
            for attempt in debugger.attempts:
                self.assertIn("attempt_number", attempt)
                self.assertIn("test_result", attempt)
                self.assertIn("error_analysis", attempt)
                self.assertIn("timestamp", attempt)
        
        print("✅ Attempt tracking test passed")
    
    def test_success_on_first_attempt(self):
        """Test that debugger succeeds if tests pass on first attempt."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file),
            max_retries=5
        )
        
        # Mock tests to pass immediately
        with patch.object(debugger, '_run_tests') as mock_run_tests:
            mock_run_tests.return_value = {
                "success": True,
                "output": "All tests passed!",
                "test_file": str(self.test_file)
            }
            
            result = debugger.debug_until_fixed()
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["attempts_count"], 1)
            self.assertIn("Successfully fixed", result["message"])
        
        print("✅ Success on first attempt test passed")
    
    def test_error_analysis(self):
        """Test that error analysis extracts error types correctly."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file)
        )
        
        # Test different error types
        test_cases = [
            {
                "output": "FAILED: AssertionError: expected 5 but got 3",
                "expected_type": "AssertionError"
            },
            {
                "output": "TypeError: unsupported operand type",
                "expected_type": "TypeError"
            },
            {
                "output": "AttributeError: 'NoneType' object has no attribute",
                "expected_type": "AttributeError"
            }
        ]
        
        for test_case in test_cases:
            test_result = {"output": test_case["output"]}
            analysis = debugger._analyze_error(test_result)
            
            self.assertEqual(analysis["error_type"], test_case["expected_type"])
        
        print("✅ Error analysis test passed")
    
    def test_search_triggered_after_attempts(self):
        """Test that search is only triggered after 2+ attempts."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file),
            max_retries=3
        )
        
        # Mock to always fail
        with patch.object(debugger, '_run_tests') as mock_run_tests, \
             patch.object(debugger, '_search_for_solution') as mock_search:
            
            mock_run_tests.return_value = {
                "success": False,
                "output": "FAILED: ValueError",
                "test_file": str(self.test_file)
            }
            mock_search.return_value = "Mock search results"
            
            result = debugger.debug_until_fixed()
            
            # Search should be called on attempts 2 and 3 only
            self.assertEqual(mock_search.call_count, 2)
            
            # Verify search results were stored in attempts
            self.assertIsNone(debugger.attempts[0]["search_results"])  # Attempt 1
            self.assertIsNotNone(debugger.attempts[1]["search_results"])  # Attempt 2
            self.assertIsNotNone(debugger.attempts[2]["search_results"])  # Attempt 3
        
        print("✅ Search triggering test passed")
    
    def test_max_retries_enforcement(self):
        """Test that loop stops at max_retries."""
        debugger = IterativeDebugger(
            test_file=str(self.test_file),
            code_file=str(self.code_file),
            max_retries=3
        )
        
        with patch.object(debugger, '_run_tests') as mock_run_tests:
            mock_run_tests.return_value = {
                "success": False,
                "output": "FAILED",
                "test_file": str(self.test_file)
            }
            
            result = debugger.debug_until_fixed()
            
            # Should stop at exactly 3 attempts
            self.assertEqual(len(debugger.attempts), 3)
            self.assertEqual(mock_run_tests.call_count, 3)
            self.assertEqual(result["status"], "max_retries")
        
        print("✅ Max retries enforcement test passed")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
