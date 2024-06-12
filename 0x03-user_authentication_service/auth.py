#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

gen_salt = bcrypt.gensalt(rounds=12)


def _hash_password(password: str) -> bytes:
    """hash user password
      Args
        password [str]: user input
      Returns:
          bytes
    """
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, gen_salt)


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
