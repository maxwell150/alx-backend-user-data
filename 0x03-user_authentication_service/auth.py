#!/usr/bin/env python3
"""auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """takes in a password string arguments and returns bytes.
    """
    return hashpw(password=password.encode(), salt=gensalt())

def _generate_uuid() -> str:
    """str repr of a new uuid
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validation
        """
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return checkpw(password=password.encode(),
                           hashed_password=usr.hashed_password)

