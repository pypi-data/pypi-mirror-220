from datetime import datetime

from config.frozen import Frozen


class Shift(Frozen):
    def __init__(self, from_ts: datetime, to_ts: datetime):
        self.__from_ts: datetime = from_ts
        self.__to_ts: datetime = to_ts

    @property
    def from_ts(self) -> datetime:
        return self.__from_ts

    @from_ts.setter
    def from_ts(self, value: datetime) -> None:
        self.__from_ts = value

    @property
    def to_ts(self) -> datetime:
        return self.__to_ts

    @to_ts.setter
    def to_ts(self, value: datetime) -> None:
        self.__to_ts = value
