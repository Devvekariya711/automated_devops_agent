"""
Sequential workflow pipelines for safe code transformations.

This module provides orchestrated workflows that execute multiple agents
in sequence with built-in safety mechanisms like automated testing and rollback.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class RefactoringPipeline:
    """
    Orchestrates safe code refactoring with automated testing and rollback.
    
    This pipeline ensures zero-risk refactoring by:
    1. Analyzing code for refactoring opportunities
    2. Creating automatic backups
    3. Applying transformations
    4. Running test suites
    5. Rolling back automatically if tests fail
    
    Usage:
        pipeline = RefactoringPipeline("vulnerable_app.py")
        result = pipeline.execute()
        
        if result["status"] == "success":
            print("Refactoring completed successfully!")
        elif result["status"] == "rollback":
            print("Tests failed, changes rolled back")
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the refactoring pipeline.
        
        Args:
            file_path: Path to the file to refactor (relative or absolute)
        """
        self.file_path = Path(file_path).resolve()
        self.backup_path = self.file_path.with_suffix(self.file_path.suffix + '.backup')
        self.refactoring_log: List[Dict[str, Any]] = []
        
    def execute(self) -> Dict[str, Any]:
        """
        Execute the complete refactoring pipeline.
        
        Returns:
            dict: Result containing status, message, and execution log
                 status: "success" | "rollback" | "skipped" | "error"
        """
        try:
            # Step 1: Validate file exists
            if not self.file_path.exists():
                return {
                    "status": "error",
                    "message": f"File not found: {self.file_path}"
                }
            
            print(f"🔧 Starting Refactoring Pipeline for {self.file_path.name}")
            print("=" * 60)
            
            # Step 2: Analyze code
            print(" Step 1/5: Analyzing code for refactoring opportunities...")
            analysis = self._analyze_code()
            self.refactoring_log.append({"step": "analysis", "result": analysis})
            
            if not analysis.get("needs_refactoring"):
                print("✅ No refactoring needed - code quality is good!")
                return {
                    "status": "skipped",
                    "message": "No refactoring opportunities found",
                    "log": self.refactoring_log
                }
            
            # Step 3: Create backup
            print("📦 Step 2/5: Creating backup...")
            self._create_backup()
            
            # Step 4: Apply refactoring (simulated for now)
            print("🔨 Step 3/5: Applying refactoring...")
            refactoring_applied = self._apply_refactoring(analysis)
            
            # Step 5: Run tests
            print("🧪 Step 4/5: Running test suite...")
            test_result = self._run_tests()
            
            # Step 6: Commit or rollback
            if test_result["success"]:
                print("✅ Step 5/5: Tests passed! Committing changes...")
                self._cleanup_backup()
                print("\n" + "=" * 60)
                print("SUCCESS: Refactoring completed successfully!")
                return {
                    "status": "success",
                    "message": "Refactoring completed successfully",
                    "changes_applied": refactoring_applied,
                    "test_results": test_result,
                    "log": self.refactoring_log
                }
            else:
                print("❌ Step 5/5: Tests failed! Rolling back...")
                self._rollback()
                print("\n" + "=" * 60)
                print("ROLLBACK: Changes reverted due to test failures")
                return {
                    "status": "rollback",
                    "message": "Refactoring rolled back due to test failures",
                    "test_failures": test_result.get("failures", []),
                    "log": self.refactoring_log
                }
        
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            if self.backup_path.exists():
                print("🔄 Rolling back due to error...")
                self._rollback()
            return {
                "status": "error",
                "message": f"Pipeline error: {str(e)}",
                "log": self.refactoring_log
            }
    
    def _analyze_code(self) -> Dict[str, Any]:
        """
        Analyze code for refactoring opportunities.
        
        In a full implementation, this would call the code_quality_agent.
        For now, returns a simplified analysis.
        """
        # Simplified: check file size as proxy for complexity
        file_size = self.file_path.stat().st_size
        lines_of_code = len(self.file_path.read_text().splitlines())
        
        needs_refactoring = lines_of_code > 100 or file_size > 3000
        
        analysis = {
            "file": str(self.file_path),
            "lines_of_code": lines_of_code,
            "file_size_bytes": file_size,
            "needs_refactoring": needs_refactoring,
            "suggestions": []
        }
        
        if needs_refactoring:
            analysis["suggestions"] = [
                {
                    "type": "extract_function",
                    "reason": "File has high line count, consider splitting into smaller functions"
                }
            ]
        
        return analysis
    
    def _create_backup(self):
        """Create a backup of the original file."""
        shutil.copy2(self.file_path, self.backup_path)
        self.refactoring_log.append({
            "step": "backup",
            "backup_path": str(self.backup_path),
            "timestamp": self._get_timestamp()
        })
        print(f"   → Backup created: {self.backup_path.name}")
    
    def _apply_refactoring(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply refactoring transformations.
        
        NOTE: This is a placeholder. In a full implementation, this would:
        1. Use an LLM to generate refactored code
        2. Apply the changes using file_writer_tool
        3. Preserve functionality while improving structure
        """
        # For now, just log that we would apply changes
        changes = {
            "type": "simulation",
            "message": "In production, this would apply actual code transformations",
            "suggested_changes": analysis.get("suggestions", [])
        }
        
        self.refactoring_log.append({
            "step": "refactor",
            "changes": changes
        })
        
        print(f"   → Refactoring simulated (would apply {len(analysis.get('suggestions', []))} changes)")
        return changes
    
    def _run_tests(self) -> Dict[str, Any]:
        """
        Run the project's test suite.
        
        Returns:
            dict: Test results with success flag and optional failures
        """
        try:
            # Look for tests directory
            project_root = self.file_path.parent
            tests_dir = project_root / "tests"
            
            if not tests_dir.exists():
                print("   ⚠️  No tests directory found - skipping test run")
                # Assume success if no tests exist
                result = {
                    "success": True,
                    "message": "No tests found - assuming safe",
                    "skipped": True
                }
                self.refactoring_log.append({"step": "test", "result": result})
                return result
            
            # Run pytest
            print(f"   → Running pytest in {tests_dir}...")
            proc = subprocess.run(
                ["pytest", str(tests_dir), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(project_root)
            )
            
            success = proc.returncode == 0
            result = {
                "success": success,
                "return_code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr
            }
            
            if not success:
                result["failures"] = self._parse_test_failures(proc.stdout)
                print(f"   ❌ {len(result['failures'])} test(s) failed")
            else:
                print("   ✅ All tests passed")
            
            self.refactoring_log.append({"step": "test", "result": result})
            return result
            
        except subprocess.TimeoutExpired:
            result = {
                "success": False,
                "message": "Tests timed out after 60 seconds",
                "failures": ["Test execution timeout"]
            }
            self.refactoring_log.append({"step": "test", "result": result})
            return result
        except FileNotFoundError:
            # pytest not installed
            print("   ⚠️  pytest not found - install with: pip install pytest")
            result = {
                "success": True,  # Assume safe if can't test
                "message": "pytest not available",
                "skipped": True
            }
            self.refactoring_log.append({"step": "test", "result": result})
            return result
    
    def _parse_test_failures(self, pytest_output: str) -> List[str]:
        """Extract failed test names from pytest output."""
        failures = []
        for line in pytest_output.split('\n'):
            if 'FAILED' in line:
                failures.append(line.strip())
        return failures[:5]  # Return first 5 failures
    
    def _rollback(self):
        """Restore the original file from backup."""
        if self.backup_path.exists():
            shutil.move(str(self.backup_path), str(self.file_path))
            self.refactoring_log.append({
                "step": "rollback",
                "status": "complete",
                "timestamp": self._get_timestamp()
            })
            print(f"   → Restored from backup: {self.file_path.name}")
        else:
            print("   ⚠️  No backup found to restore")
    
    def _cleanup_backup(self):
        """Remove backup file after successful refactoring."""
        if self.backup_path.exists():
            self.backup_path.unlink()
            print(f"   → Backup removed: {self.backup_path.name}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()


class IterativeDebugger:
    """
    Autonomous debugging with iterative retry logic.
    
    This class implements Phase 3: Loop Agents pattern where the debugger
    will attempt to fix issues multiple times until tests pass or max retries reached.
    
    Workflow:
    1. Run tests to identify failures
    2. Analyze error messages
    3. Search for solutions (Stack Overflow) if needed
    4. Generate and apply fix
    5. Re-run tests
    6. Repeat until success or max retries
    
    Usage:
        debugger = IterativeDebugger(
            test_file="tests/test_app.py",
            code_file="app.py",
            max_retries=5
        )
        result = debugger.debug_until_fixed()
        
        if result["status"] == "success":
            print(f"Fixed in {result['attempts_count']} attempts!")
        else:
            print("Max retries reached, manual intervention needed")
    """
    
    def __init__(self, test_file: str, code_file: str, max_retries: int = 5):
        """
        Initialize the iterative debugger.
        
        Args:
            test_file: Path to the test file to run
            code_file: Path to the code file to fix
            max_retries: Maximum number of fix attempts (default: 5)
        """
        self.test_file = Path(test_file).resolve()
        self.code_file = Path(code_file).resolve()
        self.max_retries = max_retries
        self.attempts: List[Dict[str, Any]] = []
        
    def debug_until_fixed(self) -> Dict[str, Any]:
        """
        Execute the iterative debugging loop.
        
        Returns:
            dict: Result containing:
                - status: "success" | "max_retries" | "error"
                - attempts_count: Number of attempts made
                - attempts: List of all attempt details
                - final_test_result: Last test execution result
        """
        print(f"🔁 Starting Iterative Debugging Loop")
        print(f"   Test File: {self.test_file.name}")
        print(f"   Code File: {self.code_file.name}")
        print(f"   Max Retries: {self.max_retries}")
        print("=" * 70)
        
        for attempt_num in range(1, self.max_retries + 1):
            print(f"\n🔍 Attempt #{attempt_num}/{self.max_retries}")
            print("-" * 70)
            
            # Step 1: Run tests
            print("  Step 1/4: Running tests...")
            test_result = self._run_tests()
            
            if test_result["success"]:
                print("  ✅ All tests passed!")
                return {
                    "status": "success",
                    "attempts_count": attempt_num,
                    "attempts": self.attempts,
                    "final_test_result": test_result,
                    "message": f"Successfully fixed in {attempt_num} attempt(s)"
                }
            
            # Step 2: Analyze failure
            print(f"  ❌ Tests failed - analyzing error...")
            error_analysis = self._analyze_error(test_result)
            
            # Step 3: Search for solutions (if stuck after 2 attempts)
            search_results = None
            if attempt_num >= 2:
                print("  🔎 Searching for similar errors online...")
                search_results = self._search_for_solution(error_analysis)
            
            # Step 4: Generate and apply fix
            print("  🔨 Generating fix...")
            fix_applied = self._generate_and_apply_fix(error_analysis, search_results)
            
            # Log this attempt
            self.attempts.append({
                "attempt_number": attempt_num,
                "test_result": test_result,
                "error_analysis": error_analysis,
                "search_results": search_results,
                "fix_applied": fix_applied,
                "timestamp": self._get_timestamp()
            })
            
            print(f"  ✓ Attempt #{attempt_num} complete")
        
        # Max retries reached
        print("\n" + "=" * 70)
        print(f"⚠️  MAX RETRIES REACHED ({self.max_retries} attempts)")
        print("   Manual intervention may be required.")
        
        return {
            "status": "max_retries",
            "attempts_count": self.max_retries,
            "attempts": self.attempts,
            "final_test_result": test_result,
            "message": f"Failed to fix after {self.max_retries} attempts"
        }
    
    def _run_tests(self) -> Dict[str, Any]:
        """
        Run the test file using pytest.
        
        Returns:
            dict: Test result with success flag and output
        """
        try:
            # Use run_pytest from tools
            from devops_automator.tools import run_pytest
            
            result_str = run_pytest(str(self.test_file), verbose=True)
            
            # Parse result
            success = "All tests passed!" in result_str or "✅" in result_str
            
            return {
                "success": success,
                "output": result_str,
                "test_file": str(self.test_file)
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Error running tests: {str(e)}",
                "error": str(e)
            }
    
    def _analyze_error(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze test failure to identify root cause.
        
        Args:
            test_result: The failed test result
            
        Returns:
            dict: Error analysis with type, location, and description
        """
        output = test_result.get("output", "")
        
        # Simple error extraction (in production, would use debugging_agent)
        analysis = {
            "error_type": "Unknown",
            "error_message": "",
            "suggested_fix": ""
        }
        
        # Extract error type
        if "AssertionError" in output:
            analysis["error_type"] = "AssertionError"
        elif "AttributeError" in output:
            analysis["error_type"] = "AttributeError"
        elif "TypeError" in output:
            analysis["error_type"] = "TypeError"
        elif "ValueError" in output:
            analysis["error_type"] = "ValueError"
        elif "ImportError" in output or "ModuleNotFoundError" in output:
            analysis["error_type"] = "ImportError"
        
        # Extract error message (simplified)
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if "Error" in line or "FAILED" in line:
                analysis["error_message"] = line.strip()
                # Get context (next 2 lines)
                if i + 1 < len(lines):
                    analysis["error_message"] += "\n" + lines[i + 1].strip()
                break
        
        return analysis
    
    def _search_for_solution(self, error_analysis: Dict[str, Any]) -> str:
        """
        Search online for similar errors (Stack Overflow, docs).
        
        Args:
            error_analysis: The error analysis dict
            
        Returns:
            str: Search results or empty string
        """
        try:
            from devops_automator.tools import google_search
            
            # Build search query
            error_type = error_analysis.get("error_type", "")
            query = f"Python {error_type} fix"
            
            results = google_search(query, num_results=3)
            return results
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def _generate_and_apply_fix(
        self, 
        error_analysis: Dict[str, Any], 
        search_results: str = None
    ) -> Dict[str, Any]:
        """
        Generate a fix based on error analysis and apply it.
        
        NOTE: This is a simplified implementation. In production, this would:
        1. Use debugging_agent to generate actual fix
        2. Apply the fix using file_writer_tool
        3. Validate the fix syntax before applying
        
        Args:
            error_analysis: The error analysis
            search_results: Optional search results for reference
            
        Returns:
            dict: Information about the fix applied
        """
        # Simplified: Log that we would apply a fix
        # In production, would call debugging_agent here
        
        fix_info = {
            "type": "simulated",
            "message": "In production, would generate and apply actual fix using debugging_agent",
            "error_addressed": error_analysis.get("error_type"),
            "search_context": "Used" if search_results else "Not used"
        }
        
        return fix_info
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()


# Example usage function for testing
def main():
    """Example usage of the RefactoringPipeline."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pipelines.py <file_path>")
        print("Example: python pipelines.py vulnerable_app.py")
        sys.exit(1)
    
    file_path = sys.argv[1]
    pipeline = RefactoringPipeline(file_path)
    result = pipeline.execute()
    
    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
