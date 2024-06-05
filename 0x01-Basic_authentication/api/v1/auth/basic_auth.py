#!/usr/bin/env python3
"""BasicAuth module"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Inherits from Auth"""
    pass

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts base64 authorization header
        Args:
            authorization_header [str]: Base64 string
        Returns:
          - Base64 part of the Authorization header for a Basic Authentication
         """
        if authorization_header is None:
            return None
        # check if the input is a string with isinstance(input, str)
        if not isinstance(authorization_header, str):
            return None
        # slicing the 4 characters of Basic from the string
        auth_var = authorization_header.rsplit(" ")
        if auth_var[0] != "Basic":
            return None
        else:
            return auth_var[1]
        # assign the above to a variable
        # compare if slice equals Basic
        # return the remaining of the slice
