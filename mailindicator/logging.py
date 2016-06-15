"""-"""
import sys


DEBUG = 3
INFO = 2
WARNING = 1
NONE = 0

_LEVEL = 0


def set_level(level):
    """Set log level."""
    global _LEVEL
    _LEVEL = level


def info(message):
    """Log info messages."""
    if _LEVEL >= INFO:
        print(message)


def debug(message):
    """Log debug messages."""
    if _LEVEL >= DEBUG:
        print(message)


def debug_ex():
    """Log exception."""
    if _LEVEL >= DEBUG:
        import traceback
        traceback.print_exc()


def error(message):
    """Log error messages."""
    sys.stderr.write(message)
    sys.stderr.write('\n')
