from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 10
    WARN = 100
    ERROR = 1000
    OFF = 10000