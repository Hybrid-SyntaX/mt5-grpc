import random
from datetime import datetime, timedelta

import pytest

from mt5_grpc.core.enums import CopyTicks, OrderType, TradeAction
from mt5_grpc.core.types import Error
from tests.util import assert_lists_are_equal, assert_values_are_equal, assert_numpy_ndarray_are_equal
from tests.integration.base import AbstractMT5TestEnv


@pytest.mark.usefixtures("mt5_test_env")
@pytest.mark.integration
class TestMT5Integration(AbstractMT5TestEnv):
    def test_symbols_total(self):
        original_result = self.mt5.symbols_total()
        mt5_client_result = self.mt5_client.symbols_total()

        assert original_result == mt5_client_result

    def test_symbol_info(self):
        original_result = self.mt5.symbol_info('USDJPY')
        mt5_client_result = self.mt5_client.symbol_info('USDJPY')

        assert_values_are_equal(original_result, mt5_client_result)

    def test_symbol_info_tick(self):
        original_result = self.mt5.symbol_info_tick('USDJPY')
        mt5_client_result = self.mt5_client.symbol_info_tick('USDJPY')

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result, exclude=['ask', 'bid'])

    def test_symbols_get(self):
        original_result = self.mt5.symbols_get('USDJPY')
        mt5_client_result = self.mt5_client.symbols_get('USDJPY')

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result)

    def test_symbol_select(self):
        original_result = self.mt5.symbol_select('USDJPY')
        mt5_client_result = self.mt5_client.symbol_select('USDJPY')

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result)

    def test_orders_total(self):
        original_result = self.mt5.orders_total()
        mt5_client_result = self.mt5_client.orders_total()

        assert original_result == mt5_client_result

    def test_orders_get(self):
        original_result = self.mt5.orders_get()
        mt5_client_result = self.mt5_client.orders_get()

        assert_lists_are_equal(original_result, mt5_client_result)

    def test_positions_total(self):
        original_result = self.mt5.positions_total()
        mt5_client_result = self.mt5_client.positions_total()

        assert original_result == mt5_client_result

    def test_positions_get(self):
        original_result = self.mt5.positions_get()
        mt5_client_result = self.mt5_client.positions_get()

        assert_lists_are_equal(original_result, mt5_client_result)

    def test_last_error(self):
        original_result = self.mt5.last_error()
        mt5_client_result = self.mt5_client.last_error()

        assert original_result == mt5_client_result

    def test_history_orders_total(self):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)

        original_result = self.mt5.history_orders_total(date_from, date_to)
        mt5_client_result = self.mt5_client.history_orders_total(date_from, date_to)

        assert original_result == mt5_client_result

    def test_history_deals_total(self):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)

        original_result = self.mt5.history_deals_total(date_from, date_to)
        mt5_client_result = self.mt5_client.history_deals_total(date_from, date_to)

        assert original_result == mt5_client_result

    def test_history_orders_get(self):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)

        original_result = self.mt5.history_orders_get(date_from, date_to)
        mt5_client_result = self.mt5_client.history_orders_get(date_from, date_to)

        assert_lists_are_equal(original_result, mt5_client_result)

    def test_history_deals_get(self):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)

        original_result = self.mt5.history_deals_get(date_from, date_to)
        mt5_client_result = self.mt5_client.history_deals_get(date_from, date_to)

        assert_lists_are_equal(original_result, mt5_client_result)

    def test_market_book_add(self):
        symbol = 'EURGBP'
        original_result = self.mt5.market_book_add(symbol)
        mt5_client_result = self.mt5_client.market_book_add(symbol)

        assert original_result == mt5_client_result

    @pytest.mark.skip("For some reason it doesn't work")
    def test_market_book_get(self):
        symbol = 'XAUUSD'
        original_result = self.mt5.market_book_get(symbol)
        mt5_client_result = self.mt5_client.market_book_get(symbol)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_lists_are_equal(original_result, mt5_client_result)

    def test_market_book_release(self):
        symbol = 'EURGBP'
        original_result = self.mt5.market_book_release(symbol)
        mt5_client_result = self.mt5_client.market_book_release(symbol)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert original_result == mt5_client_result

    @pytest.mark.skip('Causes other tests fail!')
    def test_initialize(self):
        login = self.mt5_configs['login']
        server = self.mt5_configs['server']
        password = self.mt5_configs['password']
        path = self.mt5_configs['path']

        original_result = self.mt5.initialize(path=path,
                                              login=login,
                                              server=server,
                                              password=password)
        mt5_client_result = self.mt5_client.initialize(path=path,
                                                       login=login,
                                                       server=server,
                                                       password=password)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert original_result == mt5_client_result

    @pytest.mark.skip('Causes other tests fail!')
    def test_login(self):
        login = self.mt5_configs['login']
        server = self.mt5_configs['server']
        password = self.mt5_configs['password']

        original_result = self.mt5.login(login=login,
                                         server=server,
                                         password=password)
        mt5_client_result = self.mt5_client.login(login=login,
                                                  server=server,
                                                  password=password)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert original_result == mt5_client_result

    @pytest.mark.skip('Causes other tests fail!')
    def test_shutdown(self):
        original_result = self.mt5.shutdown()
        mt5_client_result = self.mt5_client.shutdown()

        assert original_result == mt5_client_result

    def test_version(self):
        original_result = self.mt5.version()
        mt5_client_result = self.mt5_client.version()

        assert original_result == mt5_client_result

    def test_account_info(self):
        original_result = self.mt5.account_info()
        mt5_client_result = self.mt5_client.account_info()

        assert_values_are_equal(original_result, mt5_client_result)

    def test_terminal_info(self):
        original_result = self.mt5.terminal_info()
        mt5_client_result = self.mt5_client.terminal_info()

        assert_values_are_equal(original_result, mt5_client_result, exclude=['data_path', 'retransmission'])
        assert original_result.retransmission == pytest.approx(mt5_client_result.retransmission)
        assert len(original_result.data_path) == len(mt5_client_result.data_path)

    def test_copy_rates_from(self):
        symbol = 'EURUSD'
        timeframe = 1  # example timeframe
        date_from = datetime(2024, 1, 1)
        original_result = self.mt5.copy_rates_from(symbol, timeframe, date_from, 10)
        mt5_client_result = self.mt5_client.copy_rates_from(symbol, timeframe, date_from, 10)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_numpy_ndarray_are_equal(original_result, mt5_client_result)

    def test_copy_rates_from_pos(self):
        symbol = 'EURUSD'
        timeframe = 1
        start_pos = 0
        count = 10
        original_result = self.mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)
        mt5_client_result = self.mt5_client.copy_rates_from_pos(symbol, timeframe, start_pos, count)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_numpy_ndarray_are_equal(original_result, mt5_client_result)

    def test_copy_rates_range(self):
        symbol = 'EURUSD'
        timeframe = 1
        from_time = datetime(2024, 2, 1) - timedelta(days=1)
        to_time = datetime(2024, 2, 1)
        original_result = self.mt5.copy_rates_range(symbol, timeframe, from_time, to_time)
        mt5_client_result = self.mt5_client.copy_rates_range(symbol, timeframe, from_time, to_time)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'
        assert_numpy_ndarray_are_equal(original_result, mt5_client_result)

    @pytest.mark.long
    def test_copy_ticks_from(self):
        symbol = 'XAUUSD'
        from_time = datetime(2025, 5, 14) - timedelta(hours=1)
        count = 3
        flags = CopyTicks.COPY_TICKS_ALL
        original_result = self.mt5.copy_ticks_from(symbol, from_time, count, flags)
        mt5_client_result = self.mt5_client.copy_ticks_from(symbol, from_time, count, flags)

        assert type(mt5_client_result) is not Error, f'MT5 Error: {mt5_client_result}'
        assert_numpy_ndarray_are_equal(original_result, mt5_client_result)

    def test_copy_ticks_range(self):
        symbol = 'EURUSD'
        from_time = datetime(2025, 2, 1) - timedelta(minutes=1)
        to_time = datetime(2025, 2, 1)
        flags = CopyTicks.COPY_TICKS_ALL
        original_result = self.mt5.copy_ticks_range(symbol, from_time, to_time, flags)
        mt5_client_result = self.mt5_client.copy_ticks_range(symbol, from_time, to_time, flags)

        assert type(mt5_client_result) is not Error, f'MT5 Error: {mt5_client_result}'
        assert_numpy_ndarray_are_equal(original_result, mt5_client_result)

    def test_order_calc_margin(self):
        action = OrderType.ORDER_TYPE_BUY  # BUY
        symbol = 'EURUSD'
        volume = 1.0
        price = 1.2
        original_result = self.mt5.order_calc_margin(action, symbol, volume, price)
        mt5_client_result = self.mt5_client.order_calc_margin(action, symbol, volume, price)

        assert type(mt5_client_result) is not Error, f'MT5 Error: {mt5_client_result}'
        assert original_result == mt5_client_result

    def test_order_calc_profit(self):
        action = OrderType.ORDER_TYPE_BUY  # BUY
        symbol = 'EURUSD'
        volume = 1.0
        open_price = 1.2
        close_price = 1.25
        original_result = self.mt5.order_calc_profit(action, symbol, volume, open_price, close_price)
        mt5_client_result = self.mt5_client.order_calc_profit(action, symbol, volume, open_price, close_price)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'
        assert original_result == mt5_client_result

    def test_order_check(self):
        request = {
            "action": TradeAction.TRADE_ACTION_DEAL.value,  # ORDER_TYPE_SELL
            "symbol": "USDJPY",
            "volume": 0.01,
            "type": OrderType.ORDER_TYPE_BUY.value,
            "price": 1.1050,
            "sl": 0.0,
            "tp": 0.0,
            "deviation": 10,
            "magic": 123456,
            "comment": "test order",
        }
        original_result = self.mt5.order_check(request)
        mt5_client_result = self.mt5_client.order_check(request)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result, exclude=['balance', 'equity', 'margin', 'request'])
        assert_values_are_equal(original_result.request, mt5_client_result.request)

    def test_order_send(self):
        request = {
            "action": TradeAction.TRADE_ACTION_DEAL,  # ORDER_TYPE_SELL
            "symbol": "EURUSD",
            "volume": 0.02,
            "type": OrderType.ORDER_TYPE_SELL,
            "price": 1.1050,
            "sl": 0.0,
            "tp": 0.0,
            "deviation": 10,
            "magic": 123456,
            "comment": "test order send",
            "type_time": 0,
            "type_filling": 0,
        }
        original_result = self.mt5.order_send(request)
        mt5_client_result = self.mt5_client.order_send(request)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result,
                                exclude=['balance', 'equity', 'margin', 'request', 'ask', 'deal', 'order', 'request_id',
                                         'bid', 'price'])
        assert_values_are_equal(original_result.request, mt5_client_result.request)

    def test_Buy(self):
        original_result = self.mt5.Buy('USDJPY', 0.01)
        mt5_client_result = self.mt5_client.Buy('USDJPY', 0.01)

        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result,
                                exclude=['balance', 'equity', 'margin', 'request', 'ask', 'deal', 'order', 'request_id',
                                         'bid', 'price'])
        assert_values_are_equal(original_result.request, mt5_client_result.request,exclude=['price'])

    def test_Close_given_ticket(self):
        # Arrange
        symbol = 'USDJPY'
        self.mt5.Buy(symbol, 0.01)
        arrange_positions = self.mt5.positions_get(symbol=symbol)
        position = random.choice(arrange_positions)
        ticket = position.ticket

        # Act
        mt5_client_result = self.mt5_client.Close(symbol, ticket=ticket)

        # Asset
        assert type(mt5_client_result) is not tuple, f'MT5 Error: {mt5_client_result}'

        assert_positions = self.mt5.positions_get(symbol=symbol, ticket=ticket)
        assert len(assert_positions) == 0

    def test_Sell_given_ticket(self):
        original_result = self.mt5.Sell('USDJPY', 0.01)
        mt5_client_result = self.mt5_client.Sell('USDJPY', 0.01)

        assert type(mt5_client_result) is not Error, f'MT5 Error: {mt5_client_result}'

        assert_values_are_equal(original_result, mt5_client_result,
                                exclude=['balance', 'equity', 'margin', 'request', 'ask', 'deal', 'order', 'request_id',
                                         'bid','price'])
        assert_values_are_equal(original_result.request, mt5_client_result.request,exclude=['price'])

def assert_mt5_error(mt5_client_result):
    return type(
        mt5_client_result) is not tuple, f'MT5 Error (code={mt5_client_result[0]}, message={mt5_client_result[1]})'
