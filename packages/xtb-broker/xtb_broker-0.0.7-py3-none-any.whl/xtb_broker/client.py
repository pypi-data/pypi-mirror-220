import json
import socket
from time import sleep
import ssl
from random import uniform
from typing import Dict, List
from datetime import datetime
from retrying import retry

from config.constants import API_MAX_CONN_TRIES, API_MIN_SECONDS_BETWEEN_REQUESTS, API_READ_TIMEOUT, \
    XAPI_PORT_DICT, XAPI_ADDRESS, Type
from config.logger import logger
from config.exception import LoginException, GetSymbolException, GetMarginLevel, GetMarginTrade, \
    GetTradingHoursException, GetTradeRecordsException, GetTradeException, NotReceivedDataError, \
    OrderNotSentException, OrderStatusNotSentException, GetTickPricesException, retry_if_get_tick_prices_exception
from utils import unix_ts_to_ts, unix_t_to_ts, ts_to_unix_ts


last_request = datetime.now()


class JsonSocket(object):
    def __init__(self, address, port, encrypt: bool = False):
        self._ssl = encrypt 
        if not self._ssl:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ''

    def connect(self):
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                logger.error(f"SockThread Error: {msg}")
                sleep(API_MIN_SECONDS_BETWEEN_REQUESTS)
                continue
            return True
        return False

    def _send_obj(self, obj: Dict):
        self._waiting_send(json.dumps(obj))

    def _waiting_send(self, msg: str):
        if self.socket:
            sent = 0
            msg = msg.encode('utf-8')
            global last_request
            while sent < len(msg):
                sent += self.conn.send(msg[sent:])
                if (datetime.now() - last_request).total_seconds() > API_MIN_SECONDS_BETWEEN_REQUESTS:
                    last_request = datetime.now()
                else:
                    sleep(API_MIN_SECONDS_BETWEEN_REQUESTS)

    def _read(self, bytes_size: int = 4096) -> Dict:
        if not self.socket:
            raise RuntimeError("socket connection broken")
        read_time = 0
        while read_time < API_READ_TIMEOUT:
            char = self.conn.recv(bytes_size).decode()
            self._receivedData += char
            try:
                # Dict, int
                resp, size = self._decoder.raw_decode(self._receivedData)
                if size == len(self._receivedData):
                    self._receivedData = ''
                    break
                elif size < len(self._receivedData):
                    self._receivedData = self._receivedData[size:].strip()
                    break
            except ValueError as e:
                resp = str(e)
                sleep_time = uniform(0.5, 1)
                read_time += sleep_time
                sleep(sleep_time)
                continue
        if read_time > API_READ_TIMEOUT:
            raise NotReceivedDataError("Xtb API is not responding and no data is being received")
        logger.debug(f'Received: {resp}')
        return resp

    def _read_obj(self) -> Dict:
        return self._read()

    def close(self):
        logger.debug("Closing socket")
        self._close_socket()
        if self.socket is not self.conn:
            logger.debug("Closing connection socket")
            self._close_connection()

    def _close_socket(self):
        self.socket.close()

    def _close_connection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    def _get_encrypt(self):
        return self._ssl

    def _set_encrypt(self, encrypt):
        pass

    timeout = property(_get_timeout, _set_timeout, doc='Get/set the socket timeout')
    address = property(_get_address, _set_address, doc='read only property socket address')
    port = property(_get_port, _set_port, doc='read only property socket port')
    encrypt = property(_get_encrypt, _set_encrypt, doc='read only property socket port')
    
    
class XtbClient(JsonSocket):
    def __init__(self, mode: str):
        super(XtbClient, self).__init__(address=XAPI_ADDRESS, port=XAPI_PORT_DICT[mode], encrypt=True)
        if not self.connect():
            raise Exception(f"Cannot connect to streaming on "
                            f"{XAPI_ADDRESS}: {XAPI_PORT_DICT[mode]} after {API_MAX_CONN_TRIES} retries")

    def execute(self, params: Dict) -> Dict:
        self._send_obj(params)
        return self._read_obj()    

    def disconnect(self):
        self.close()

    @staticmethod
    def command_template(command_name, arguments=None) -> Dict:
        return dict([('command', command_name), ('arguments', arguments or dict())])
        
    def command(self, command_name, arguments=None):
        return self.execute(self.command_template(command_name, arguments))

    def login(self, user_id, password, app_name='') -> str:
        arguments: Dict = dict(userId=user_id, password=password, appName=app_name)
        resp = self.command(command_name='login', arguments=arguments)
        if resp['status']:
            return resp['streamSessionId']
        else:
            logger.debug(f"Error {resp['errorCode']}, {resp['errorDescr']}")
            if not (resp['errorCode'] == 'BE118' and resp['errorDescr'] == 'User already logged'):
                raise LoginException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def get_symbol(self, symbol: str) -> Dict:
        arguments: Dict = dict(symbol=symbol)
        resp = self.command(command_name="getSymbol", arguments=arguments)
        if resp['status']:
            return resp['returnData']
        else:
            logger.error(f"Error {resp['errorCode']}, {resp['errorDescr']}")
            raise GetSymbolException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def get_trades(self, opened_only: bool = True) -> List:
        arguments: Dict = dict(openedOnly=opened_only)
        # try:
        resp = self.command(command_name="getTrades", arguments=arguments)
        if resp['status']:
            return resp['returnData']
        else:
            raise GetTradeException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    @retry(retry_on_exception=retry_if_get_tick_prices_exception,
           stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def get_tick_prices(self,
                        symbols: List[str], level: int = 0, timestamp: int = ts_to_unix_ts(datetime.now())) -> List:
        arguments: Dict = dict(symbols=symbols, level=level, timestamp=timestamp)
        resp = self.command(command_name="getTickPrices", arguments=arguments)
        if resp['status']:
            if resp['returnData']['quotations']:
                return resp['returnData']['quotations']
            else:
                raise GetTickPricesException(f"Error EMPTY, No tick prices received")
        raise GetTickPricesException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def get_chart_range_request(
            self, period_value: int, symbol_name: str, start_unix_ts: int, end_unix_ts: int) -> List:
        arguments: Dict = dict(info=dict(
            symbol=symbol_name,
            period=period_value,
            start=start_unix_ts,
            end=end_unix_ts))
        resp = self.command(command_name="getChartRangeRequest", arguments=arguments)
        if resp['status']:
            return resp['returnData']['rateInfos']
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")
            return []
        
    def get_server_time(self) -> datetime:
        resp = self.command(command_name="getServerTime")
        if resp['status']:
            return unix_ts_to_ts(resp['returnData']['time'])
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")

    def get_trading_hours(self, symbols: List[str]) -> Dict[str, Dict[int, List[Dict[str, datetime]]]]:
        arguments: Dict = dict(symbols=symbols)
        resp = self.command(command_name="getTradingHours", arguments=arguments)
        if resp['status']:
            trading_hours = dict()
            for symbol in resp['returnData']:
                trading_hours[symbol['symbol']] = dict()
                for day in symbol['trading']:
                    if not day['day'] in trading_hours[symbol['symbol']]:
                        trading_hours[symbol['symbol']][day['day']] = []
                    trading_hours[symbol['symbol']][day['day']].append(
                        dict(from_ts=unix_t_to_ts(day['fromT']), to_ts=unix_t_to_ts(day['toT'])))
            return trading_hours
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")
            raise GetTradingHoursException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def get_trade_records(self, orders: List[int]) -> List:
        arguments: Dict = dict(orders=orders)
        resp = self.command(command_name="getTradeRecords", arguments=arguments)
        if resp['status']:
            return resp['returnData']
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")
            raise GetTradeRecordsException(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def trade_transaction(self, trade: Dict, _type: int) -> int:
        keeping_keys = ['cmd', 'comment', 'expiration', 'offset', 'order', 'sl', 'symbol', 'tp', 'volume']
        arguments: Dict = dict(tradeTransInfo={key: trade[key] for key in keeping_keys})
        arguments['tradeTransInfo']['type'] = _type
        if _type == Type.OPEN:
            arguments['tradeTransInfo']['price'] = trade['open_price']
        elif _type == Type.CLOSE:
            arguments['tradeTransInfo']['price'] = trade['close_price']
        resp = self.command(command_name="tradeTransaction", arguments=arguments)
        if resp['status']:
            return resp['returnData']['order']
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")
            raise OrderNotSentException(f"Error {resp['errorCode']}:: {resp['errorDescr']}")

    def trade_transaction_status(self, transacting_order: int) -> Dict:
        arguments: Dict = dict(order=transacting_order)
        resp = self.command(command_name="tradeTransactionStatus", arguments=arguments)
        if resp['status']:
            return resp['returnData']
        else:
            logger.error(f"Error {resp['errorCode']}:: {resp['errorDescr']}")
            raise OrderStatusNotSentException(f"Error {resp['errorCode']}:: {resp['errorDescr']}")

    def get_margin_level(self) -> Dict:
        resp = self.command(command_name="getMarginLevel")
        if resp['status']:
            return resp['returnData']
        else:
            logger.error(f"Error {resp['errorCode']}, {resp['errorDescr']}")
            raise GetMarginLevel(f"Error {resp['errorCode']}, {resp['errorDescr']}")

    def get_free_margin(self) -> float:
        return self.get_margin_level()['margin_free']

    def get_margin_trade(self, symbol: str, volume: float) -> float:
        arguments: Dict = dict(symbol=symbol, volume=volume)
        resp = self.command(command_name="getMarginTrade", arguments=arguments)
        if resp['status']:
            return resp['returnData']['margin']
        else:
            logger.error(f"Error {resp['errorCode']}, {resp['errorDescr']}")
            raise GetMarginTrade(f"Error {resp['errorCode']}, {resp['errorDescr']}")
