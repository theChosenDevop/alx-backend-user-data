#!/usr/bin/env python3
"""filtered_logger module"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> str:
        """Initialize Object"""
        self.fields = fields

        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """returns a formatted log
        Arguments
          record [str]: string record
        """
        msg = super(RedactingFormatter, self).format(record)
        
        filtered = filter_datum(
                self.fields, self.REDACTION, msg, self.SEPARATOR)
        return filtered


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
    pattern = "({})=[^{}]+".format({'|'.join(fields)})=[^{separator}]*
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
