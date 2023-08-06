from typing import List, Dict, Optional
from datetime import datetime
from retrying import retry

from config.exception import ArbitragePartiallyClosedException, TradeNotFoundException, \
    retry_if_arbitrage_partially_closed_exception
from config.frozen import Frozen
from config.constants import Cmd
from config.logger import logger
from models.position import Position
from models.symbol import Symbol
from models.shift import Shift
from models.trade import Trade
from utils import get_today_ini, get_today_end
from xtb import Xtb


class Arbitrage(Frozen):
    def __init__(self,
                 xtb: Xtb,
                 name: str,
                 active: bool,
                 tp: float,
                 sl: float,
                 positions: List[Dict]):
        self.__name: str = name
        self.__active: bool = active
        self.__tp: float = tp
        self.__sl: float = sl
        self.__positions: List[Position] = self.__init_positions(xtb=xtb, setup_positions=positions)
        self.__shift: Optional[Shift] = self.__extract_shift()
        self.__status: str = ""
        self.__profit: float = 0
        self.__action: str = ""

    def __init_positions(self, xtb: Xtb, setup_positions: List[Dict]) -> List[Position]:
        positions = []
        for setup_position in setup_positions:
            if "trade" not in setup_position or not setup_position['trade']:
                setup_position['trade'] = dict(
                    cmd=getattr(Cmd(), setup_position['direction']),
                    volume=setup_position['volume'],
                    symbol=setup_position['symbol'],
                    comment=self.__name)
            positions.append(Position(xtb=xtb, **setup_position))
        return positions

    @property
    def name(self) -> str:
        return self.__name

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def active_on_off(self) -> str:
        return "On" if self.__active else "Off"

    @property
    def tp(self) -> float:
        return self.__tp

    @property
    def sl(self) -> float:
        return self.__sl

    @property
    def shift(self) -> Shift:
        return self.__shift

    @property
    def positions(self) -> List[Position]:
        return self.__positions

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, value: str) -> None:
        self.__action = value

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        self.__status = value

    @property
    def symbols(self) -> List[Symbol]:
        return list(map(lambda position: position.symbol, self.positions))

    @property
    def orders(self) -> List[int]:
        return list(map(lambda position: position.order, self.positions))

    @property
    def trades(self) -> List[Trade]:
        return list(map(lambda position: position.trade, self.positions))

    @property
    def is_working(self):
        return all(map(lambda p: p.is_working, self.positions))

    @property
    def is_completely_accepted(self):
        accepted = list(map(lambda p: p.trade.accepted, self.positions))
        return sum(accepted) == len(accepted)

    @property
    def is_partially_failed(self):
        accepted = list(map(lambda p: p.trade.accepted, self.positions))
        return 0 < sum(accepted) < len(accepted)

    @property
    def is_completely_failed(self):
        accepted = list(map(lambda p: p.trade.accepted, self.positions))
        return 0 == sum(accepted)

    def __extract_shift(self) -> Optional[Shift]:
        if self.is_working:
            shift = Shift(from_ts=get_today_ini(), to_ts=get_today_end())
            for position in self.__positions:
                shift.from_ts = max([shift.from_ts, position.shift.from_ts])
                shift.to_ts = min([shift.to_ts, position.shift.to_ts])
            return shift

    def __get_trades(self, xtb: Xtb):
        trades = xtb.get_client().get_trade_records(orders=self.orders)
        for position in self.positions:
            trade = list(filter(lambda t: t['order'] == position.order, trades))
            if trade:
                position.trade = Trade(trade_raw=list(trade)[0])
            else:
                logger.debug(f"No trade found for order '{position.order} - {position.symbol.symbol}'")
                raise TradeNotFoundException(f"No trade found for order {position.order}")

    def is_operable(self, closing_threshold: int):
        return (self.shift.to_ts - datetime.now()).total_seconds() > closing_threshold

    @property
    def profit(self) -> float:
        return round(sum(map(lambda p: p.profit, self.positions)), 2)

    @retry(retry_on_exception=retry_if_arbitrage_partially_closed_exception,
           stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def transact(self, xtb: Xtb, _type: int) -> None:
        keep_opening = True
        for idx, position in enumerate(self.positions):
            if keep_opening:
                if not position.trade.accepted:
                    position.trade.transact(xtb=xtb, _type=_type)
                    self.positions[idx].action = position.trade.transaction.status
                if not position.trade.accepted:
                    keep_opening = False

        if self.is_completely_accepted:
            logger.debug("Arbitrage process was SUCCESSFUL and is COMPLETELY CLOSED")
            self.action = "closed"
        if self.is_partially_failed:
            logger.critical("Arbitrage process has FAILED and is PARTIALLY CLOSED")
            self.action = "PARTIALLY closed"
            raise ArbitragePartiallyClosedException("Arbitrage process has FAILED and is PARCIALLY CLOSED")
        if self.is_completely_failed:
            self.action = "COMPLETELY open"
            logger.warning("Arbitrage process has FAILED and is COMPLETELY OPEN")
