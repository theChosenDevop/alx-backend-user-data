#!/usr/bin/env python3
"""filtered_logger module"""
import re
import logging
import mysql.connector
import os
from typing import List, Tuple


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


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

    def __init__(self, fields: List[str]):
        """Initialize Object"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns a formatted log
        Arguments
          record [str]: string record
        """
        msg = super(RedactingFormatter, self).format(record)

        f_msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return f_msg
