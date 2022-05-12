#!/usr/bin/env python3
"""personal data
"""
from typing import List
import re
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated
    """
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log.setFormatter(formatter)
    log.addHandler(handler)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to mysql database
    """
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD")
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(user=username, password=password,
                                   host=host, database=dbname)
