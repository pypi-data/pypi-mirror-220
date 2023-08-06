from typing import Dict, Optional
from datetime import datetime

from xtb_config.frozen import Frozen
from xtb_config.constants import WEEKDAY
from xtb_models.timetable import Timetable
from xtb_models.shift import Shift

from xtb import Xtb



class Symbol(Frozen):
    def __init__(self, xtb: Xtb, symbol: str):
        symbol_dict: Dict = xtb.get_client().get_symbol(symbol=symbol)
        self.__symbol: str = symbol_dict['symbol']
        self.__currency: str = symbol_dict['currency']
        self.__currency_profit: str = symbol_dict['currencyProfit']
        self.__contract_size: str = symbol_dict['contractSize']
        self.__precision: str = symbol_dict['precision']
        self.__bid: str = symbol_dict['bid']
        self.__ask: str = symbol_dict['ask']
        self.__swap_long: str = symbol_dict['swapLong']
        self.__swap_short: str = symbol_dict['swapShort']
        self.__spread: float = symbol_dict['spreadRaw']
        self.__timetable: Timetable = xtb.get_symbol_timetable(symbol=symbol)
        
    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.__symbol = value

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, value: str) -> None:
        self.__currency = value

    @property
    def currency_profit(self) -> str:
        return self.__currency_profit

    @property
    def contract_size(self) -> str:
        return self.__contract_size

    @contract_size.setter
    def contract_size(self, value: str) -> None:
        self.__contract_size = value

    @property
    def precision(self) -> str:
        return self.__precision

    @precision.setter
    def precision(self, value: str) -> None:
        self.__precision = value

    @property
    def bid(self) -> str:
        return self.__bid

    @bid.setter
    def bid(self, value: str) -> None:
        self.__bid = value

    @property
    def ask(self) -> str:
        return self.__ask

    @ask.setter
    def ask(self, value: str) -> None:
        self.__ask = value

    @property
    def swap_long(self) -> str:
        return self.__swap_long

    @swap_long.setter
    def swap_long(self, value: str) -> None:
        self.__swap_long = value

    @property
    def swap_short(self) -> str:
        return self.__swap_short

    @swap_short.setter
    def swap_short(self, value: str) -> None:
        self.__swap_short = value

    @property
    def timetable(self) -> Timetable:
        return self.__timetable

    @timetable.setter
    def timetable(self, value: Timetable) -> None:
        self.__timetable = value

    @property
    def spread(self) -> float:
        return self.__spread

    @spread.setter
    def spread(self, value: float) -> None:
        self.__spread = value

    def get_active_shift(self) -> Optional[Shift]:
        for shift in getattr(self.timetable, WEEKDAY[datetime.today().isoweekday()]):
            if shift.from_ts < datetime.now() < shift.to_ts:
                return shift
