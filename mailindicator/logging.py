import sys


DEBUG = 3
INFO = 2
WARNING = 1
NONE = 0

_level = 0


def setLevel(level):
    global _level
    _level = level


def info(message):
    if _level >= INFO:
        print(message)


def debug(message):
    if _level >= DEBUG:
        print(message)


def error(message):
    sys.stderr.write(message)
    sys.stderr.write('\n')
