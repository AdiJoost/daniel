from enum import Enum

class PricePoints(Enum):
    OPEN = 'open'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
    ADJUSTED_CLOSE = 'adjusted_close'
    VOLUME = 'volume'