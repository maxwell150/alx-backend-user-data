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

    def create_session(self, email: str) -> str:
        """return the session id
        """
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            usr.session_id = _generate_uuid()
            return usr.session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """takes a single session_id string argument and returns the corresponding User or None.
        """
        try:
            usr = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        if usr.session_id is None:
            return None
        else:
            return usr

    def destroy_session(self, user_id: int) -> None:
        """takes a single user_id integer argument and returns None.
        """
        try:
            usr = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        usr.session_id = None

