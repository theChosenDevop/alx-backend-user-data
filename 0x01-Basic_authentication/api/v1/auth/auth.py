#!/usr/bin/env python3
"""Auth Module"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Auth class"""
    def __init__(self):
        """ïnitialaization of object"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a given path requires authentication
        Args:
          path: The path to check
          excluded_paths: A list of paths that do not require
                          authentication
        Returns:
          - False if does not require authentication or otherwise True
        """
        if path is None:
            return True
        if excluded_paths is None:
            return True
        # ensure path has a trailing slash
        if not path.endswith('/'):
            path += '/'
        for x_path in excluded_paths:
            if not x_path.endswith('/'):
                x_path += '/'
            if fnmatch.fnmatch(path, x_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns:
          - None - request
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns:
          - None - request
        """
        return None
