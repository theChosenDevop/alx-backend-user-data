#!/usr/bin/env python3
"""SessionAuth Module"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Inherits from superclass Auth"""

    def __init__(self):
        """initialization of class"""
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id
        Args:
            user_id [str]: user identification
        Returns:
            None if user_id is None or not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        Args:
            user_id [str]: user identification
        Returns:
            the value (the User ID) for the key session_id in the
            dictionary user_id_by_session_id.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value

        Args:
            request: The user request.

        Returns:
            User: The User instance or None if not found.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        for session in self.user_id_by_session_id:
            if session_id == session:
                user_inst = self.user_id_by_session_id[session_id]
                return User.get(user_inst)
