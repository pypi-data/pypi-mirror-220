class FrozenError(AttributeError):
    pass


class GenericException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}, {self.message}"


class GetSymbolException(GenericException):
    pass


class GetMarginLevel(GenericException):
    pass


class GetMarginTrade(GenericException):
    pass


class LoginException(GenericException):
    pass


class GetTradeException(GenericException):
    pass


class GetTickPricesException(GenericException):
    pass


def retry_if_get_tick_prices_exception(exception):
    # logger.warning(f"{exception}")
    return isinstance(exception, GetTickPricesException)


class GetTradingHoursException(GenericException):
    pass


class GetTradeRecordsException(GenericException):
    pass


class OrderNotSentException(GenericException):
    pass


def retry_if_order_not_sent_exception(exception):
    # logger.warning(f"{exception}")
    return isinstance(exception, OrderNotSentException)


class OrderPendingException(GenericException):
    pass


def retry_if_order_not_accepted_exception(exception):
    # logger.warning(f"{exception}")
    return isinstance(exception, OrderPendingException) or isinstance(exception, OrderStatusNotSentException)


class OrderStatusNotSentException(GenericException):
    pass


class ArbitragePartiallyClosedException(GenericException):
    pass


def retry_if_arbitrage_partially_closed_exception(exception):
    # logger.warning(f"{exception}")
    return isinstance(exception, ArbitragePartiallyClosedException)


class TradeNotFoundException(GenericException):
    pass


class NotReceivedDataError(GenericException):
    pass
