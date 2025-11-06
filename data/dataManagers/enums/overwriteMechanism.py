from enum import Enum

class OverwriteMechanism(Enum):
    APPEND = "APPEND"
    OVERWRITE = "OVERWRITE"
    ERROR_ON_EXISTS = "ERROR_ON_EXISTS"