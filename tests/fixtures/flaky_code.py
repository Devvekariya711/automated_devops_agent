"""
Flaky test fixture for Phase 3 testing.

This file intentionally contains bugs that need iterative fixes.
Used to test the IterativeDebugger retry loop functionality.
"""


def divide_numbers(a, b):
    """
    Divide two numbers.
    
    BUG: No zero division handling
    """
    return a / b  # Will fail if b == 0


def calculate_average(numbers):
    """
    Calculate average of a list of numbers.
    
    BUG: No empty list handling
    """
    total = sum(numbers)
    count = len(numbers)
    return total / count  # Will fail if list is empty


def get_first_element(items):
    """
    Get the first element from a list.
    
    BUG: No index checking
    """
    return items[0]  # Will fail if list is empty


def parse_integer(value):
    """
    Parse a string to integer.
    
    BUG: No error handling for invalid input
    """
    return int(value)  # Will fail for non-numeric strings

