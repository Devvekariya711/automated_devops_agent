"""
Sample vulnerable code for testing comprehensive audit functionality.

This file intentionally contains:
1. Security vulnerabilities (SQL injection, hardcoded credentials)
2. High complexity functions
3. PEP 8 violations
4. Missing test coverage

DO NOT use this code in production!
"""

import sqlite3
import os


# SECURITY ISSUE: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"


def get_user_data(user_id):
    """
    Fetch user data from database.
    
    SECURITY VULNERABILITY: SQL Injection
    This function is vulnerable to SQL injection attacks.
    """
    # VULNERABILITY: String concatenation in SQL query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id  # ❌ SQL Injection!
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def complex_business_logic(data, mode, options, filters, flags, params):
    """
    Process business logic with multiple branches.
    
    QUALITY ISSUE: High cyclomatic complexity
    This function has too many decision points and should be refactored.
    """
    result = []
    
    # Too many nested conditions - high complexity
    if mode == "standard":
        if options.get("validate"):
            if filters:
                for item in data:
                    if item.get("active"):
                        if flags.get("priority"):
                            if params.get("threshold", 0) > 10:
                                if item.get("score", 0) > params["threshold"]:
                                    result.append(item)
                            else:
                                result.append(item)
                        elif flags.get("secondary"):
                            if item.get("category") == "important":
                                result.append(item)
                    else:
                        if flags.get("include_inactive"):
                            result.append(item)
            else:
                result = data
        else:
            result = data
    elif mode == "advanced":
        if options.get("filter_nulls"):
            result = [x for x in data if x is not None]
        else:
            result = data
    else:
        result = []
    
    return result


def process_payment(card_number, amount):
    """
    Process payment transaction.
    
    SECURITY ISSUE: Logging sensitive data
    """
    # ❌ Logging credit card number - PCI DSS violation!
    print(f"Processing payment for card {card_number} amount ${amount}")
    
    # Simulated payment processing
    if len(card_number) == 16:
        return {"status": "success", "transaction_id": "TXN001"}
    else:
        return {"status": "failed", "error": "Invalid card"}


# PEP 8 VIOLATIONS
def BadFunctionName( x,y,z ):  # Wrong naming, bad spacing
    """This function violates PEP 8 style guidelines."""
    VeryLongVariableNameThatViolatesPEP8=x+y+z  # No spaces around =
    if(VeryLongVariableNameThatViolatesPEP8>100):  # Unnecessary parentheses
        return True
    else:
        return False


class user_class:  # ❌ Class name should be UserClass (PascalCase)
    """User management class with style violations."""
    
    def __init__(self,name,email):  # ❌ Missing spaces after commas
        self.name=name  # ❌ No spaces around =
        self.email=email
    
    def get_data(self):
        return {'name':self.name,'email':self.email}  # ❌ No spaces after colons


# MISSING ERROR HANDLING
def read_config_file(filename):
    """
    Read configuration file.
    
    QUALITY ISSUE: No error handling for file operations
    """
    # ❌ No try/except - will crash if file doesn't exist
    with open(filename, 'r') as f:
        config = f.read()
    return config


# UNUSED IMPORTS (above)
# import os is imported but never used


if __name__ == "__main__":
    # Demo code - intentionally insecure
    print("This is sample vulnerable code for testing only!")
    
    # This would be vulnerable to SQL injection:
    # user_data = get_user_data("1 OR 1=1")  # SQL Injection attack
