#!/usr/bin/env python3
"""auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """takes in a password string arguments and returns bytes.
    """
    return hashpw(password=password.encode(), salt=gensalt())

