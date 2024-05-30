#!/usr/bin/env python3
"""filtered_logger module
"""
import re
from typing import List


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
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
