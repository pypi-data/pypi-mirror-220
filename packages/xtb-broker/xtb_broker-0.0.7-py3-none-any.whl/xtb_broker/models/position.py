from typing import Dict, Optional

from config.frozen import Frozen
from config.constants import Cmd
from models.symbol import Symbol
from models.shift import Shift
from models.trade import Trade

from xtb import Xtb


class Position(Frozen):
    def __init__(self,
                 xtb: Xtb,
                 order: int,
                 direction: str,
                 symbol: str,
                 volume: float,
                 trade: Dict):
        self.__direction: int = getattr(Cmd, direction)
        self.__order: int = order
        self.__symbol: Symbol = Symbol(xtb=xtb, symbol=symbol)
        self.__trade: Trade = Trade(trade_raw=trade)
        self.__shift: Optional[Shift] = self.__symbol.get_active_shift()
        self.__volume: float = volume
        self.__action: str = ""

    @property
    def direction(self) -> int:
        return self.__direction

    @property
    def order(self) -> int:
        return self.__order

    @order.setter
    def order(self, value: int) -> None:
        self.__order = value

    @property
    def trade(self) -> Trade:
        return self.__trade

    @trade.setter
    def trade(self, value: Dict) -> None:
        self.__frozen__ = False
        self.__trade = value
        self.__frozen__ = True

    @property
    def symbol(self) -> Symbol:
        return self.__symbol

    @property
    def shift(self) -> Shift:
        return self.__shift

    @shift.setter
    def shift(self, value: Shift) -> None:
        self.__shift = value

    @property
    def volume(self) -> float:
        return self.__volume

    @volume.setter
    def volume(self, value: float) -> None:
        self.__volume = value

    @property
    def is_working(self) -> bool:
        return bool(self.__shift)

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, value: str) -> None:
        self.__action = value

    @property
    def name(self) -> str:
        return f"{self.symbol} {self.direction} {self.volume}"

    @property
    def profit(self) -> float:
        if self.trade:
            return round(self.trade.profit + self.trade.storage, 2)
        return 0
