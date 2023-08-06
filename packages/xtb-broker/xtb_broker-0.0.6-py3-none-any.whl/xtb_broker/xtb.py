from typing import Optional, Dict
from retrying import retry
from datetime import datetime
import sys
import os

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '.')))
from xtb_config.constants import WEEKDAY
from xtb_models.timetable import Timetable
from xtb_models.shift import Shift
from utils import ts_to_unix_ts
import client
from client import XtbClient



# Declared at cold-start, but only initialized if/when the function executes (initializing them lazily on demand)
xtb_client: Optional[XtbClient] = None


class Xtb:
    def __init__(self, mode: str):
        self.__mode: str = mode
        self.__xtb_client: Optional[XtbClient] = None

    def __get_client(
        self,
        _client: Optional[client.XtbClient] = None,
        reconnect: bool = False
    ) -> Optional[client.XtbClient]:
        try:
            if not _client or reconnect:
                client_new: XtbClient = get_xtb_client(self.__mode)
                return client_new
        except Exception as e:
            raise Exception(f'__get_client:: {e}')

    def get_client(self, reconnect: bool = False) -> XtbClient:
        global xtb_client
        xtb_client_new: Optional[XtbClient] = self.__get_client(xtb_client, reconnect)
        if xtb_client_new:
            # create xtb_client -> initializing them lazily on demand
            xtb_client = xtb_client_new
        return xtb_client

    def is_now_server_time(self, server_time: datetime = None) -> bool:
        if server_time is None:
            server_time = self.get_client().get_server_time().replace(microsecond=0)
        now = datetime.now().replace(microsecond=0)
        return abs(now.timestamp() - server_time.timestamp()) < 60

    def get_symbol_timetable(self, symbol: str) -> Timetable:
        timetable = Timetable()
        timetable.__frozen__ = False
        for day, shifts in self.get_client().get_trading_hours([symbol])[symbol].items():
            timetable.__setattr__(
                WEEKDAY[day].lower(), [Shift(from_ts=shift['from_ts'], to_ts=shift['to_ts']) for shift in shifts])
        timetable.__frozen__ = True
        return timetable

    def get_tick_price(self, symbol: str, level: int = 0, timestamp: int = ts_to_unix_ts(datetime.now())) -> Dict:
        return self.get_client().get_tick_prices(symbols=[symbol], level=level, timestamp=timestamp)[0]

    def get_trade_record(self, order: int) -> Dict:
        return self.get_client().get_trade_records(orders=[order])[0]


@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_xtb_client(mode: str) -> XtbClient:
    return XtbClient(mode)

