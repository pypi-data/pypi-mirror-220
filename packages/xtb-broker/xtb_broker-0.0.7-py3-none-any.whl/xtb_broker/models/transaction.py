from typing import Optional, Dict

from config.frozen import Frozen
from config.constants import Status


class Transaction(Frozen):
    def __init__(self, order: int):
        self.__order: int = order
        self.__status: str = ''
        self.__message: str = ''
        self.__custom_comment: Optional[str] = None
        self.__ask: float = 0.0
        self.__bid: float = 0.0

    def __repr__(self) -> str:
        return str(self.__to_dict())

    def __to_dict(self) -> Dict:
        return dict(
            order=self.__order,
            status=self.__status,
            message=self.__message,
            custom_comment=self.__custom_comment,
            ask=self.__ask,
            bid=self.__bid)

    @property
    def order(self) -> int:
        return self.__order

    @order.setter
    def order(self, value: int) -> None:
        self.__order = value

    @property
    def status(self) -> int:
        return self.__status

    @status.setter
    def status(self, value: int) -> None:
        self.__status = value

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str) -> None:
        self.__message = value

    @property
    def custom_comment(self) -> str:
        return self.__custom_comment

    @custom_comment.setter
    def custom_comment(self, value: str) -> None:
        self.__custom_comment = value

    @property
    def ask(self) -> float:
        return self.__ask

    @ask.setter
    def ask(self, value: float) -> None:
        self.__ask = value

    @property
    def bid(self) -> float:
        return self.__bid

    @bid.setter
    def bid(self, value: float) -> None:
        self.__bid = value

    @property
    def accepted(self) -> bool:
        return self.status == Status.ACCEPTED