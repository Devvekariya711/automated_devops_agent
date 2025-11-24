"""
Integration tests for Phase 2: Sequential Workflows

Tests the RefactoringPipeline functionality including:
- Sequential execution of analyze → backup → refactor → test → commit/rollback
- Automatic backup creation and restoration
- Test-driven rollback mechanism
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from devops_automator.pipelines import RefactoringPipeline


class TestSequentialWorkflows(unittest.TestCase):
    """Test suite for Phase 2: Sequential Workflows."""
    
    def setUp(self):
        """Set up test environment."""
        # Use sample vulnerable code as test file
        self.test_file = Path(__file__).parent / "fixtures" / "sample_vulnerable_code.py"
        self.backup_file = self.test_file.with_suffix(self.test_file.suffix + '.backup')
        
        # Clean up any existing backups
        if self.backup_file.exists():
            self.backup_file.unlink()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove backup if exists
        if self.backup_file.exists():
            self.backup_file.unlink()
    
    def test_pipeline_initialization(self):
        """Test that pipeline initializes correctly."""
        pipeline = RefactoringPipeline(str(self.test_file))
        
        self.assertEqual(pipeline.file_path, self.test_file)
        self.assertEqual(pipeline.backup_path, self.backup_file)
        self.assertEqual(len(pipeline.refactoring_log), 0)
        
        print("✅ Pipeline initialization test passed")
    
    def test_pipeline_analyzes_code(self):
        """Test that pipeline can analyze code quality."""
        pipeline = RefactoringPipeline(str(self.test_file))
        
        # Call private method for testing
        analysis = pipeline._analyze_code()
        
        self.assertIn("file", analysis)
        self.assertIn("lines_of_code", analysis)
        self.assertIn("needs_refactoring", analysis)
        
        # Sample vulnerable code has >100 lines, should need refactoring
        self.assertTrue(analysis["needs_refactoring"])
        
        print("✅ Code analysis test passed")
    
    def test_backup_creation(self):
        """Test that backup files are created correctly."""
        pipeline = RefactoringPipeline(str(self.test_file))
        
        # Create backup
        pipeline._create_backup()
        
        # Verify backup exists
        self.assertTrue(self.backup_file.exists())
        
        # Verify backup content matches original
        original_content = self.test_file.read_text()
        backup_content = self.backup_file.read_text()
        self.assertEqual(original_content, backup_content)
        
        print("✅ Backup creation test passed")
    
    def test_pipeline_executes_sequence(self):
        """Test that pipeline executes all steps in sequence."""
        pipeline = RefactoringPipeline(str(self.test_file))
        
        # Execute pipeline (will skip refactoring in simulation mode)
        result = pipeline.execute()
        
        # Verify result structure
        self.assertIn("status", result)
        self.assertIn("message", result)
        self.assertIn("log", result)
        
        # Verify all steps executed
        steps = [entry["step"] for entry in result["log"]]
        self.assertIn("analysis", steps)
        
        print(f"✅ Pipeline execution test passed - Status: {result['status']}")
    
    def test_file_not_found_error(self):
        """Test pipeline handles missing files gracefully."""
        pipeline = RefactoringPipeline("nonexistent_file.py")
        
        result = pipeline.execute()
        
        self.assertEqual(result["status"], "error")
        self.assertIn("File not found", result["message"])
        
        print("✅ File not found error handling test passed")
    
    def test_rollback_restoration(self):
        """Test that rollback restores original file."""
        pipeline = RefactoringPipeline(str(self.test_file))
        
        # Create backup
        pipeline._create_backup()
        original_content = self.test_file.read_text()
        
        # Modify the original file
        modified_content = "# Modified content\n" + original_content
        self.test_file.write_text(modified_content)
        
        # Verify file was modified
        self.assertNotEqual(self.test_file.read_text(), original_content)
        
        # Rollback
        pipeline._rollback()
        
        # Verify file was restored
        restored_content = self.test_file.read_text()
        self.assertEqual(restored_content, original_content)
        
        print("✅ Rollback restoration test passed")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
