#!/usr/bin/env python
"""filtered_logger module"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] % (name)s % (levelname)s % (asctime) - 15s:
        %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(fields: list, redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated
    Argument:
       fields [List] : list of strings representing all fields to obfuscate
       redaction [Str] : representing by what the field will be obfuscated
       message [str] : representing the log line
       separator [str] : representing by which character is
                        separating all fields in the log line (message)
    """
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
