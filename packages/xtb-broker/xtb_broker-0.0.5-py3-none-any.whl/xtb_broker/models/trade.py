from typing import Dict, Optional
from retrying import retry

from xtb_config.frozen import Frozen
from xtb_config.exception import OrderPendingException, \
    retry_if_order_not_sent_exception, retry_if_order_not_accepted_exception
from xtb_config.constants import Type, CMD, Cmd, STATUS, Status
from xtb_config.logger import logger
from xtb import Xtb
from xtb_models.transaction import Transaction


class Trade(Frozen):
    def __init__(self, trade_raw: Dict):
        trade_raw['order'] = trade_raw.get('order', 0)
        trade_raw['offset'] = trade_raw.get('offset', 0)
        trade_raw['sl'] = trade_raw.get('sl', 0)
        trade_raw['tp'] = trade_raw.get('tp', 0)
        trade_raw['profit'] = trade_raw.get('profit', 0)
        trade_raw['expiration'] = trade_raw.get('expiration', 0)
        trade_raw['storage'] = trade_raw.get('storage', 0)
        self.__order: Optional[int] = trade_raw['order']
        self.__cmd: int = trade_raw['cmd']
        self.__comment: str = trade_raw['comment']
        self.__offset: Optional[float] = trade_raw['offset']
        self.__sl: Optional[float] = trade_raw['sl']
        self.__tp: Optional[float] = trade_raw['tp']
        self.__symbol: str = trade_raw['symbol']
        self.__volume: float = trade_raw['volume']
        self.__profit: Optional[float] = trade_raw['profit']
        self.__storage: Optional[float] = trade_raw['storage']
        self.__raw: Dict = trade_raw
        self.__transaction: Optional[Transaction] = None


    @property
    def order(self) -> int:
        return self.__order

    # TODO: la mayoría de los setters sobran
    @order.setter
    def order(self, value: int) -> None:
        self.__order = value

    @property
    def cmd(self) -> int:
        return self.__cmd

    @cmd.setter
    def cmd(self, value: int) -> None:
        self.__cmd = value

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str) -> None:
        self.__comment = value

    @property
    def offset(self) -> float:
        return self.__offset

    @offset.setter
    def offset(self, value: float) -> None:
        self.__offset = value

    @property
    def sl(self) -> float:
        return self.__sl

    @sl.setter
    def sl(self, value: float) -> None:
        self.__sl = value

    @property
    def tp(self) -> float:
        return self.__tp

    @tp.setter
    def tp(self, value: float) -> None:
        self.__tp = value

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.__symbol = value

    @property
    def volume(self) -> float:
        return self.__volume

    @volume.setter
    def volume(self, value: float) -> None:
        self.__volume = value

    @property
    def raw(self) -> Dict:
        return self.__raw

    @raw.setter
    def raw(self, value: Dict) -> None:
        self.__raw = value

    @property
    def profit(self) -> float:
        return self.__profit

    @profit.setter
    def profit(self, value: float) -> None:
        self.__profit = value

    @property
    def storage(self) -> float:
        return self.__storage

    @storage.setter
    def storage(self, value: float) -> None:
        self.__storage = value

    @property
    def transaction(self) -> Transaction:
        return self.__transaction

    @transaction.setter
    def transaction(self, value: Transaction) -> None:
        self.__transaction = value

    @property
    def accepted(self) -> bool:
        try:
            return self.transaction.accepted
        except:
            return False

    def transact(self, xtb: Xtb, _type: int) -> None:
        symbol = xtb.get_client().get_symbol(symbol=self.__symbol)
        if _type == Type.OPEN:
            if self.cmd == Cmd.BUY:
                self.raw['open_price'] = symbol['ask']
            elif self.cmd == Cmd.SELL:
                self.raw['open_price'] = symbol['bid']
        self.send_transaction(xtb=xtb, _type=_type)
        self.check_order_sent(xtb=xtb)

    @retry(retry_on_exception=retry_if_order_not_sent_exception,
           stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def send_transaction(self, xtb: Xtb, _type: int) -> None:
        # TODO: check lotMin del symbol antes de mandar transaction y devolver una exception
        self.transaction = Transaction(order=xtb.get_client().trade_transaction(trade=self.raw, _type=_type))

    @retry(retry_on_exception=retry_if_order_not_accepted_exception,
           stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def check_order_sent(self, xtb: Xtb):
        try:
            transaction = xtb.get_client().trade_transaction_status(transacting_order=self.transaction.order)
            self.transaction.status = STATUS[transaction['requestStatus']]
            self.transaction.message = transaction['message']
            self.transaction.custom_comment = transaction['customComment']
            self.transaction.ask = transaction['ask']
            self.transaction.bid = transaction['bid']
            if self.transaction.status == Status.ACCEPTED:
                logger.debug(f"Trade order '{self.order} - {self.symbol} - {CMD[self.cmd]}' is CLOSED. "
                             f"Transaction order is {self.transaction.order}")
            elif self.transaction.status == Status.PENDING:
                logger.warning(f"Trade order '{self.order} - {self.symbol} - {CMD[self.cmd]}' is PENDING. "
                               f"Transaction order is {self.transaction}")
                raise OrderPendingException(f"Trade order '{self.order} is PENDING. "
                                            f"Closing order is {self.transaction}")
            elif self.transaction.status == Status.ERROR:
                logger.error(f"Trade order '{self.order} - {self.symbol} - {CMD[self.cmd]}' has FAILED. "
                             f"Transaction: {self.transaction}")
            elif self.transaction.status == Status.REJECTED:
                logger.error(f"Trade order '{self.order} - {self.symbol} - {CMD[self.cmd]}' has been REJECTED. "
                             f"Transaction order is {self.transaction}")
        except OrderPendingException:
            self.transaction.status = Status.PENDING
        except Exception as e:
            logger.error(e)
