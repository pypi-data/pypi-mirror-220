from typing import Dict
from dataclasses import dataclass

# Wrapper name and version
WRAPPER_NAME: str = 'python'
WRAPPER_VERSION: str = '2.5.0'

# XAPI connection
XAPI_ADDRESS: str = 'xapi.xtb.com'
XAPI_PORT_DICT: Dict = dict(DEMO=5124, REAL=5112)

# API inter-command timeout (in ms)
API_MIN_SECONDS_BETWEEN_REQUESTS: float = 0.5

# max connection tries
API_MAX_CONN_TRIES: int = 3
API_READ_TIMEOUT: int = 1120

STATUS: Dict = {
    0: "ERROR",
    1: "PENDING",
    3: "ACCEPTED",
    4: "REJECTED"}


@dataclass(frozen=True)
class Status(object):
    ERROR: str = 'ERROR'
    PENDING: str = 'PENDING'
    ACCEPTED: str = 'ACCEPTED'
    REJECTED: str = 'REJECTED'


WEEKDAY: Dict = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday"}


@dataclass(frozen=True)
class Weekday(object):
    monday: int = 'monday'
    tuesday: int = 'tuesday'
    wednesday: int = 'wednesday'
    thursday: int = 'thursday'
    friday: int = 'friday'
    saturday: int = 'saturday'
    sunday: int = 'sunday'


@dataclass(frozen=True)
class TransactionSide(object):
    BUY: int = 0
    SELL: int = 1
    BUY_LIMIT: int = 2
    SELL_LIMIT: int = 3
    BUY_STOP: int = 4
    SELL_STOP: int = 5


@dataclass(frozen=True)
class TransactionType(object):
    ORDER_OPEN: int = 0
    ORDER_CLOSE: int = 2
    ORDER_MODIFY: int = 3
    ORDER_DELETE: int = 4


@dataclass(frozen=True)
class Type:
    OPEN: int = 0
    PENDING: int = 1
    CLOSE: int = 2
    MODIFY: int = 3
    DELETE: int = 4


@dataclass(frozen=True)
class LogLevel:
    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    WARNING: str = "WARNING"
    ERROR: str = "ERROR"
    CRITICAL: str = "CRITICAL"

LOG_LEVEL: str = LogLevel.INFO


@dataclass(frozen=True)
class Cmd:
    BUY: int = 0
    SELL: int = 1


CMD: Dict = {0: "BUY", 1: "SELL"}


@dataclass(frozen=True)
class Period:
    M1: int = 1
    M5: int = 5
    M15: int = 15
    M30: int = 30
    H1: int = 60
    H4: int = 240
    D1: int = 1440
    W1: int = 10080
    MN1: int = 43200
