"""
Tests for login functionality.

This test will FAIL until the autonomous agent fixes buggy_login.py!
The agent should detect the bug and autonomously fix it.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import buggy_login
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo.buggy_login import authenticate_user, get_user_role


def test_admin_login_success():
    """
    Test that admin login returns 200 status code.
    
    THIS TEST WILL FAIL due to the bug in buggy_login.py!
    The autonomous agent should fix it.
    """
    result = authenticate_user("admin", "secret")
    assert result == 200, f"Admin login should return 200 (success), but got {result}"


def test_invalid_login():
    """Test that invalid credentials return 401."""
    result = authenticate_user("admin", "wrongpassword")
    assert result == 401, f"Invalid login should return 401 (unauthorized), got {result}"


def test_user_role_admin():
    """Test that admin role is correctly retrieved."""
    role = get_user_role("admin")
    assert role == "administrator", f"Admin role should be 'administrator', got '{role}'"


def test_user_role_unknown():
    """Test that unknown users get guest role."""
    role = get_user_role("unknown_user")
    assert role == "guest", f"Unknown user should get 'guest' role, got '{role}'"
