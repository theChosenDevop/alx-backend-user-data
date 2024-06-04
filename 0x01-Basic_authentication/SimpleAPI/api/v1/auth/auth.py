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
        """
        Returns:
          - False False - path
        """
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
