#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """hash user password
      Args
        password [str]: user input
      Returns:
          bytes
    """
    gen_salt = bcrypt.gensalt(rounds=12)
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, gen_salt)


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new users and returns error
           and error user exist
           Args:
              email [str]: user email to be checked on database
              password [str]: user password to hashed
           Returns: User object
        """
        storage = self._db
        try:
            find_user = storage.find_user_by(email=email)
            if find_user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = storage.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login
            Args:
            email [str]: user email
            password [str]: user password
            Returns: bool
        """
        storage = self._db
        hashed_pwd = password.encode('utf-8')
        try:
            user = storage.find_user_by(email=email)
            return bcrypt.checkpw(hashed_pwd, user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """checks user email and attach session id to it
           and stores in storage
            Args:
                email [str]: user email
            Returns: session id
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """returns corresponding user or None if user don't exist
           Args:
                session_id [str]: user session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: str) -> None:
        """updates the corresponding user’s session ID to None
           Args:
                user_id [str]: user id
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except (NoResultFound, InvalidRequestError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Function resets password token
           Args:
                email [str]: user email
           Returns: reset_token
        """
        if email is None:
            return ("None")
        storage = self._db
        try:
            user = storage.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except (NoResultFound, InvalidRequestError):
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Use reset_token to find user and update hashed_password
            Args:
                reset_token [str]: user reset token
                password [str]: user password
            Returns: None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hashed_password = _hash_password(password)
            user.hashed_password = new_hashed_password
            user.reset_token = None
            return None
        except (NoResultFound, InvalidRequestError):
            raise ValueError()
