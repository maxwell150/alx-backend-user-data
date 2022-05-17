#!/usr/bin/env python3
"""API authentication module
"""


from flask import request
from typing import TypeVar, List


class Auth:
    """ API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path[-1] == '/':
            path = path[:-1]

        for i in range(len(excluded_paths)):
            if excluded_paths[i][-1] == '/':
                excluded_paths[i] = excluded_paths[i][:-1]
            if excluded_paths[i][-1] == '*':
                path_len = len(excluded_paths[i][:-1])
                if path[:path_len - 1] in excluded_paths[i][:-1]:
                    return False

        if path in excluded_paths:
            return False

        return True


    def authorization_header(self, request=None) -> str:
        """authorization header
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]


    def current_user(self, request=None) -> TypeVar('User'):
        """current user returns None - request
        """
        return None
