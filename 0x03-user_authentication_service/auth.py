#!/usr/bin/env python3
"""auth module
"""
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """takes in a password string arguments and returns bytes.
    """
    return hashpw(password=password.encode(), salt=gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """return user obj
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password=password)
            return self._db.add_user(email=email, hashed_password=hashed)
        else:
            raise ValueError(f"User {email} already exists")



