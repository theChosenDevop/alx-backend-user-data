#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
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


def _generate_uuid():
    """Returns a string representation of a new UUID
    """
    id = uuid.uuid4
    return str(id)


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
