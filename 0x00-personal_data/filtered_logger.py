#!/usr/bin/env python3
"""filtered_logger module"""
import re
import logging
from typing import List
import mysql.connection
import os


PII_FIELDS = ('name', 'email', 'phonenumber', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated
    Argument:
        fields [List] : list of strings representing all fields to obfuscate
        redaction [Str] : representing by what the field will be obfuscated
        message [str] : representing the log line
        separator [str] : representing by which character is
                        separating all fields in the log line (message)
    """
    pattern = rf"({'|'.join(fields)})=[^{separator }]*"
    redacted_message = re.sub(
            pattern, lambda m: f"{m.group(1)}={redaction}", message)
    return redacted_message.replace(separator, separator + " ")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> str:
        """Initialize Object"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns a formatted log
        Arguments
          record [str]: string record
        """
        msg = super(RedactingFormatter, self).format(record)

        filtered = filter_datum(
                self.fields, self.REDACTION, msg, self.SEPARATOR)
        return filtered


def get_logger() -> logging.Logger:
    """creates a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects user to msql server"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
            host=host, user=user, password=pwd, database=db)

    return connection


ded main():
    """get user info"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM USERS;")
    fields = cursor.column_name
    for row in curaor:
        msg = "".join("{}={}; ".format(key, value) for key, value
                      in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()
