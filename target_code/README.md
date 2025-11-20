# Target Code Directory

This directory contains **example and test code** used to demonstrate the capabilities of the DevOps automation agents.

## Contents

### Test Fixtures

- **`vulnerable_app.py`** - Intentionally vulnerable code containing:
  - SQL injection vulnerability
  - Logic errors (division by zero)
  - Missing input validation
  - Used to test the Security Scanner Agent

### Test Files

- **`test_agent.py`** - Unit tests for root agent routing logic
- **`agent_test.py`** - Additional agent tests
- **`tools_test.py`** - Tests for custom tools
- **`supporting_agents_test.py`** - Tests for specialized agents

### Reference Code (Duplicates)

The files `agent.py`, `tools.py`, and `supporting_agents.py` in this directory are copies from the main `devops_automator` package. They may be used as:
- Examples for the agents to analyze
- Test fixtures for file reading operations
- Documentation references

> **Note**: The authoritative source code is in the `devops_automator/` directory, not here.

## Purpose

This directory demonstrates:
1. **Security Scanner** - Detecting vulnerabilities in `vulnerable_app.py`
2. **Debugging Agent** - Fixing logic errors
3. **Unit Test Generator** - Creating tests for problematic code
4. **File Reader Tool** - Safely reading project files

## Running Tests

```bash
# Run all tests
python -m pytest target_code/ -v

# Run specific test file
python target_code/test_agent.py
```

## ⚠️ Important

**DO NOT** use `vulnerable_app.py` in production or as a template for real applications. It contains deliberately insecure code for testing purposes only.
