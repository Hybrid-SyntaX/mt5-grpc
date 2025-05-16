from abc import abstractmethod, ABCMeta
from datetime import datetime


class AbstractMetaTrader5(metaclass=ABCMeta):
    @abstractmethod
    def copy_rates_range(self, symbol, timeframe, date_from, date_to):
        pass

    @abstractmethod
    def copy_rates_from(self, symbol, timeframe, date_from, count):
        pass

    @abstractmethod
    def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
        pass

    @abstractmethod
    def copy_ticks_from(self, symbol, date_from, count, flags):
        pass

    @abstractmethod
    def copy_ticks_range(self, symbol: str, date_from: datetime, date_to: datetime, flags):
        pass

    @abstractmethod
    def symbols_get(self, group: str = None):
        pass

    @abstractmethod
    def symbol_info_tick(self, symbol: str):
        pass

    @abstractmethod
    def symbol_info(self, symbol: str):
        pass

    @abstractmethod
    def symbol_select(self, symbol: str):
        pass

    @abstractmethod
    def symbols_total(self):
        pass

    @abstractmethod
    def order_send(self, trade_request):
        pass

    @abstractmethod
    def order_check(self, trade_request):
        pass

    @abstractmethod
    def order_calc_profit(self, action, symbol, volume, price_open, price_close):
        pass

    @abstractmethod
    def order_calc_margin(self, action, symbol, volume, price):
        pass

    @abstractmethod
    def orders_total(self):
        pass

    @abstractmethod
    def orders_get(self, symbol=None, ticket=None, group=None):
        pass

    @abstractmethod
    def positions_total(self):
        pass

    @abstractmethod
    def positions_get(self, symbol=None, ticket=None, group=None):
        pass

    @abstractmethod
    def history_orders_total(self, date_from, date_to):
        pass

    @abstractmethod
    def history_orders_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        pass

    @abstractmethod
    def history_deals_total(self, date_from, date_to):
        pass

    @abstractmethod
    def history_deals_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        pass

    @abstractmethod
    def last_error(self):
        pass

    @abstractmethod
    def market_book_add(self, symbol):
        pass

    @abstractmethod
    def market_book_release(self, symbol):
        pass

    @abstractmethod
    def market_book_get(self, symbol):
        pass

    @abstractmethod
    def initialize(self, path, server, login, password):
        pass

    @abstractmethod
    def login(self, server, login, password):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def version(self):
        pass

    @abstractmethod
    def account_info(self):
        pass

    @abstractmethod
    def terminal_info(self):
        pass

    @abstractmethod
    def Close(self, symbol, *, comment=None, ticket=None):
        pass

    @abstractmethod
    def Buy(self, symbol, volume, price=None, *, comment=None, ticket=None):
        pass

    @abstractmethod
    def Sell(self, symbol, volume, price=None, *, comment=None, ticket=None):
        pass
