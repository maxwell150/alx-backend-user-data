#!/usr/bin/env python3
"""encrypting user passwd in db"""


import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
