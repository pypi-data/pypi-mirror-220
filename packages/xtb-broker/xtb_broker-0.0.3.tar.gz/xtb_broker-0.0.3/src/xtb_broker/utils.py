import time
from datetime import datetime, date, timedelta
import sys


def ts_to_unix_ts(ts: datetime) -> int:
    return int(time.mktime(ts.timetuple())*1000)


def unix_ts_to_ts(unix_ts: int) -> datetime:
    return datetime.fromtimestamp(unix_ts/1000)


def unix_t_to_ts(unix_t: int):
    return datetime.combine(date.today(), datetime.min.time()) + timedelta(seconds=unix_t/1000)


def get_today_ini() -> datetime:
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


def get_today_end() -> datetime:
    return get_today_ini() + timedelta(days=1)


def f_name() -> str:
    return sys._getframe(1).f_code.co_name


