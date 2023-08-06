from typing import List, Optional

from models.shift import Shift
from config.frozen import Frozen


class Timetable(Frozen):
    def __init__(self):
        self.__monday: List[Shift] = []
        self.__tuesday: List[Shift] = []
        self.__wednesday: List[Shift] = []
        self.__thursday: List[Shift] = []
        self.__friday: List[Shift] = []
        self.__saturday: List[Shift] = []
        self.__sunday: List[Shift] = []

    @property
    def monday(self) -> Optional[List[Shift]]:
        return self.__monday

    @monday.setter
    def monday(self, value: List[Shift]) -> None:
        self.__monday = value

    @property
    def tuesday(self) -> Optional[List[Shift]]:
        return self.__tuesday

    @tuesday.setter
    def tuesday(self, value: List[Shift]) -> None:
        self.__tuesday = value

    @property
    def wednesday(self) -> Optional[List[Shift]]:
        return self.__wednesday

    @wednesday.setter
    def wednesday(self, value: List[Shift]) -> None:
        self.__wednesday = value

    @property
    def thursday(self) -> Optional[List[Shift]]:
        return self.__thursday

    @thursday.setter
    def thursday(self, value: List[Shift]) -> None:
        self.__thursday = value

    @property
    def friday(self) -> Optional[List[Shift]]:
        return self.__friday

    @friday.setter
    def friday(self, value: List[Shift]) -> None:
        self.__friday = value

    @property
    def saturday(self) -> Optional[List[Shift]]:
        return self.__saturday

    @saturday.setter
    def saturday(self, value: List[Shift]) -> None:
        self.__saturday = value

    @property
    def sunday(self) -> Optional[List[Shift]]:
        return self.__sunday

    @sunday.setter
    def sunday(self, value: List[Shift]) -> None:
        self.__sunday = value

