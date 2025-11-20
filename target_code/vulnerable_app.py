"""
⚠️  INTENTIONALLY VULNERABLE TEST CODE ⚠️

This file contains deliberately insecure code for testing the Security Scanner Agent.
DO NOT use this code in production!

Security Vulnerabilities Included:
1. SQL Injection (line 9) - User input concatenated directly into SQL query
2. Logic Error (line 24) - Division operation that can cause ZeroDivisionError
3. Missing Input Validation - No validation on discount parameter

This code is used to demonstrate and test:
- The Security Scanner Agent's ability to detect OWASP Top 10 vulnerabilities
- The Debugging Agent's capability to identify and fix logic errors
- The Unit Test Generator's edge case detection

For secure code examples, see the devops_automator module.
"""

import sqlite3

def get_user_data(username):
    """
    Retrieves user data from the database.
    """
    # SECURITY FLAW: SQL Injection Vulnerability
    # The user input is directly concatenated into the query string.
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Executing the unsafe query
    cursor.execute(query)
    return cursor.fetchall()

def calculate_discount(price, discount):
    """
    Calculates the final price after discount.
    """
    # BUG: ZeroDivisionError potential if price is 0 (logic error)
    # BUG: No validation if discount is greater than price
    return price / discount

def main():
    print("Welcome to the app")
    user = get_user_data("admin' OR '1'='1") # Simulating an attack
    print(user)

if __name__ == "__main__":
    main()