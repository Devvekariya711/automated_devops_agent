"""
Benchmark: SQL Injection Vulnerability

Expected Issues:
- SQL injection in get_user_by_id() (Critical)
- SQL injection in search_users() (Critical)
- Hardcoded database credentials (High)
"""

import sqlite3

# SECURITY ISSUE: Hardcoded credentials
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASS = "password123"  # Critical: Hardcoded password


def get_user_by_id(user_id):
    """
    CRITICAL VULNERABILITY: SQL Injection
    Should use parameterized queries.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SQL Injection vulnerability - string concatenation
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return result


def search_users(search_term):
    """
    CRITICAL VULNERABILITY: SQL Injection
    Vulnerable to: ' OR '1'='1
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results


def delete_user(user_id):
    """Another SQL injection point."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    conn.commit()
    conn.close()
