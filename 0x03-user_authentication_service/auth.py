#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt

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
