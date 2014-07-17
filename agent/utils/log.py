import os
import traceback
import logging
import logging.handlers

import agent.utils.variables as gvars

LOG_FORMAT = '%(levelname)s : %(asctime)s : %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'

LoggingFormatter = None

_logger = None
_initialized = False


class LogLevel():
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


def debug(message):
    if _initialized:
        _logger.debug(message)


def info(message):
    if _initialized:
        _logger.info(message)


def warning(message):
    if _initialized:
        _logger.warning(message)


def error(message):
    if _initialized:
        _logger.error(message)


def critical(message):
    if _initialized:
        _logger.critical(message)


def exception(e):
    if _initialized:
        log_message = "Exception: {0}".format(e)
        _logger.error(log_message)
        _logger.error(traceback.format_exc())


def _get_log_level(level):
    if level == 'info':
        return logging.INFO

    elif level == 'debug':
        return logging.DEBUG

    elif level == 'warning':
        return logging.WARNING

    elif level == 'error':
        return logging.ERROR

    elif level == 'critical':
        return logging.CRITICAL

    return logging.DEBUG


def add_log_handler(filename, roll_interval='midnight', backupCount=7):
    """Adds handler to _logger with formatting using LOG_FORMAT and
    LOG_DATE_FORMAT.
    """
    global _logger

    handler = logging.handlers.TimedRotatingFileHandler(
        filename, when=roll_interval, backupCount=backupCount
    )

    handler.setFormatter(
        logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    )

    _logger.addHandler(handler)


def remove_log_handler(handler):
    """Removes handler from _logger."""
    global _logger

    handler.close()
    _logger.removeHandler(handler)


def remove_all_handlers():
    """Removes all handlers from logger."""
    for handler in _logger.handlers:
        remove_log_handler(handler)


def initialize(log_level=LogLevel.DEBUG):
    """Initialize logging for the agent.

    @return: Nothing
    """
    global _initialized
    global _logger

    _logger = logging.getLogger('log.all')
    _logger.setLevel(_get_log_level(log_level))
    _logger.propagate = False

    add_log_handler(gvars.LOG_FILE)

    _initialized = True

