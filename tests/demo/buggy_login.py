"""
Deliberately buggy login function for autonomous fix demo.

BUG: Returns HTTP 500 (server error) instead of 200 (success) for valid logins.
"""

def authenticate_user(username, password):
    """
    Authenticates a user with username and password.
    
    Returns:
        int: HTTP status code
            - 200: Successful authentication
            - 401: Unauthorized (invalid credentials)
    """
    # 🐛 BUG: Wrong status code!
    # Should return 200 for successful authentication, not 500!
    if username == "admin" and password == "secret":
        return 500  # ❌ BUG HERE - Should be 200
    return 401  # Unauthorized


def get_user_role(username):
    """Returns the role of the authenticated user."""
    roles = {
        "admin": "administrator",
        "user": "standard_user"
    }
    return roles.get(username, "guest")
