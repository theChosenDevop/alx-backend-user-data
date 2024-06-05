#!/usr/bin/env python3
"""Auth Module"""
from flask import request
from api.v1 import app
from typing import List, TypeVar


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
        if path is None or excluded_paths is None:
            return True
        # ensure path has a trailing slash
        if not path.endswith('/'):
            path += '/'
        # ensure excluded_paths have a slash
        excluded_paths = [
                route_path if route_path.endswith('/')
                else route_path + '/' for route_path in excluded_paths
                ]
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns:
          - None - request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns:
          - None - request
        """
        return None
