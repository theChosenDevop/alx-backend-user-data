#!/usr/bin/env python3
"""BasicAuth module"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Inherits from Auth"""
    pass

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts base64 authorization header
        Args:
            authorization_header [str]: string input
        Returns:
          - Base64 part of the Authorization header for a Basic Authentication
         """
        if authorization_header is None:
            return None
        # check if the input is a string with isinstance(input, str)
        if not isinstance(authorization_header, str):
            return None
        # split the string characters of Basic by space
        auth_var = authorization_header.rsplit(" ")
        if auth_var[0] != "Basic":
            return None
        else:
            return auth_var[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes base64 string
        Args:
            base64_authorization_header [str]: base64 string
        Returns:
            - decoded value of Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # convert it to bytes object
            string_object = base64_authorization_header.encode('ascii')
            # decode it to base64 bytes
            base64_object = base64.b64decode(string_object)
            # decode it to utf string
            return base64_object.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials
        Args:
            base64_authorization_header [str]: base64 string
        Returns:
            - User details
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # split decoded_base64_authorization_header into index
        email, pwd = decoded_base64_authorization_header.split(":")
        return email, pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns User instance base on email and password
        Args:
            - user_email [str] - input
            - user_pwd [str] - input
        """
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        if user_email is None or not isinstance(user_email, str):
            return None

        User.load_from_file()
        users = User.search({'email': user_email})
        if users is not None:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None
