from datetime import datetime
from typing import List, Tuple, Union, Dict

from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp

from mt5_grpc.generated_proto import messages_pb2

from mt5_grpc.generated_proto import services_pb2_grpc
from mt5_grpc.core.enums import TimeFrame, CopyTicks, OrderType
from mt5_grpc.mt5_grpc_client.mappings import ticks_to_numpy, rates_to_numpy
from mt5_grpc.core.types import SymbolInfo, Tick, AccountInfo, TerminalInfo, TradeRequest, TradeOrder, TradeDeal, \
    OrderSendResult, OrderCheckResult, PositionType, TradePosition
from mt5_grpc.core import types
from mt5_grpc.core.abstracts import AbstractMetaTrader5
from mt5_grpc.util.type_mapping import auto_map


class GRPCMetaTrader5(AbstractMetaTrader5):
    stub: services_pb2_grpc.MetaTrader5ServiceStub

    def __init__(self, channel):
        self.channel = channel
        self.stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)

    def copy_rates_range(self, symbol: str, timeframe: TimeFrame, date_from: datetime, date_to: datetime):
        stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)

        # timeframe = map_obj('timeframe', 'python', 'grpc', timeframe)

        date_from_timestamp = Timestamp()
        date_from_timestamp.FromDatetime(date_from)
        date_to_timestamp = Timestamp()
        date_to_timestamp.FromDatetime(date_to)

        request = messages_pb2.CopyRatesRangeRequest(
            timeframe=timeframe,
            symbol=symbol,
            date_from=date_from_timestamp,
            date_to=date_to_timestamp
        )
        response = stub.CopyRatesRange(request)

        if response.error.code == 0:
            return rates_to_numpy(response.rates)

        return None

    def copy_rates_from(self, symbol: str, timeframe: TimeFrame, date_from: datetime, count: int):
        stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)

        # timeframe = map_obj('timeframe', 'python', 'grpc', timeframe)

        date_from_timestamp = Timestamp()
        date_from_timestamp.FromDatetime(date_from)

        request = messages_pb2.CopyRatesFromRequest(
            timeframe=timeframe,
            symbol=symbol,
            date_from=date_from_timestamp,
            count=count)
        response = stub.CopyRatesFrom(request)

        if response.error.code == 0:
            return rates_to_numpy(response.rates)

        return None

    def copy_rates_from_pos(self, symbol: str, timeframe: TimeFrame, start_pos: int, count: int):
        # timeframe = map_obj('timeframe', 'python', 'grpc', timeframe)

        request = messages_pb2.CopyRatesFromPosRequest(
            timeframe=timeframe,
            symbol=symbol,
            start_pos=start_pos,
            count=count
        )
        response = self.stub.CopyRatesFromPos(request)

        if response.error.code == 0:
            return rates_to_numpy(response.rates)

        return response.error.code, response.error.message

    def copy_ticks_from(self, symbol: str, date_from: datetime, count: int, flags: CopyTicks):
        stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)

        date_from_timestamp = Timestamp()
        date_from_timestamp.FromDatetime(date_from)

        request = messages_pb2.CopyTicksFromRequest(
            symbol=symbol,
            date_from=date_from_timestamp,
            count=count,
            flags=flags
        )
        response = stub.CopyTicksFrom(request)

        if response.error.code == 0:
            return ticks_to_numpy(response.ticks)

        return None

    def copy_ticks_range(self, symbol: str, date_from: datetime, date_to: datetime, flags: CopyTicks):
        date_from_timestamp = Timestamp()
        date_from_timestamp.FromDatetime(date_from)

        date_to_timestamp = Timestamp()
        date_to_timestamp.FromDatetime(date_to)

        request = messages_pb2.CopyTicksRangeRequest(
            symbol=symbol,
            date_from=date_from_timestamp,
            date_to=date_to_timestamp,
            flags=flags
        )
        response = self.stub.CopyTicksRange(request)

        if response.error.code == 0:
            return ticks_to_numpy(response.ticks)

        return response.error.code, response.error.message

    def symbols_get(self, group=None) -> List[SymbolInfo]:
        response: messages_pb2.SymbolsGetResponse = self.stub.SymbolsGet(messages_pb2.SymbolsGetRequest(group=group))
        symbol_infos = []
        if response.error.code == 0:
            symbol_infos = list(map(lambda s: auto_map(s, SymbolInfo, 'right'), response.symbols))

        return symbol_infos

    def symbol_info_tick(self, symbol: str) -> Union[Tick, Tuple[int, str]]:
        response: messages_pb2.SymbolInfoTickResponse = self.stub.SymbolInfoTick(
            messages_pb2.SymbolInfoTickRequest(symbol=symbol))
        if response.error.code == 0:
            return auto_map(response.tick, Tick, 'right')

        return response.error.code, response.error.message

    def symbol_info(self, symbol: str) -> Union[SymbolInfo, Tuple[int, str]]:
        response: messages_pb2.SymbolInfoResponse = self.stub.SymbolInfo(messages_pb2.SymbolInfoRequest(symbol=symbol))
        if response.error.code == 0:
            return auto_map(response.symbol_info, SymbolInfo, 'right')
        return response.error.code, response.error.message

    def symbol_select(self, symbol: str):
        response: messages_pb2.SymbolSelectResponse = self.stub.SymbolSelect(
            messages_pb2.SymbolSelectRequest(symbol=symbol))
        if response.error.code == 0:
            return response.success
        return response.error.code, response.error.message

    def symbols_total(self):
        response: messages_pb2.SymbolsTotalResponse = self.stub.SymbolsTotal(Empty())
        if response.error.code == 0:
            return response.symbols_total
        return response.error.code, response.error.message

    def order_send(self, request: Union[Dict, TradeRequest]):
        if type(request) is dict:
            request = TradeRequest(**request)

        trade_request = auto_map(request, messages_pb2.TradeRequest, 'left')
        response: messages_pb2.OrderSendResponse = self.stub.OrderSend(
            messages_pb2.OrderSendRequest(trade_request=trade_request))
        if response.error.code == 0:
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            order_send_result = auto_map(response.order_send_result, OrderSendResult, 'right',
                                         manual={'request': map_request})

            return order_send_result

        return response.error.code, response.error.message

    def order_check(self, request: Union[Dict, TradeRequest]):
        if type(request) is dict:
            request = TradeRequest(**request)

        trade_request = auto_map(request, messages_pb2.TradeRequest, 'left')
        response: messages_pb2.OrderCheckResponse = self.stub.OrderCheck(
            messages_pb2.OrderCheckRequest(trade_request=trade_request))

        if response.error.code == 0:
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            order_check_result = auto_map(response.order_check_result, OrderCheckResult, 'right',
                                          manual={'request': map_request})
            return order_check_result
        return response.error.code, response.error.message

    def order_calc_profit(self, action: OrderType, symbol, volume, price_open, price_close):
        response = self.stub.OrderCalcProfit(messages_pb2.OrderCalcProfitRequest(action=action,
                                                                                 symbol=symbol,
                                                                                 volume=volume,
                                                                                 price_open=price_open,
                                                                                 price_close=price_close))

        if response.error.code == 0:
            return response.profit
        return response.error.code, response.error.message

    def order_calc_margin(self, action: OrderType, symbol, volume, price):
        response = self.stub.OrderCalcMargin(messages_pb2.OrderCalcMarginRequest(action=action,
                                                                                 symbol=symbol,
                                                                                 volume=volume,
                                                                                 price=price))

        if response.error.code == 0:
            return response.margin
        return response.error.code, response.error.message

    def orders_total(self):
        response = self.stub.OrdersTotal(Empty())

        if response.error.code == 0:
            return response.total
        return response.error.code, response.error.message

    def orders_get(self, symbol=None, ticket=None, group=None):
        response = self.stub.OrdersGet(messages_pb2.OrdersGetRequest(symbol=symbol, ticket=ticket, group=group))

        if response.error.code == 0:
            orders = tuple(map(lambda s: auto_map(s, TradeOrder, 'right'), response.orders))

            return orders

        return response.error.code, response.error.message

    def positions_total(self):
        response = self.stub.PositionsTotal(Empty())

        if response.error.code == 0:
            return response.total
        return response.error.code, response.error.message

    def positions_get(self, symbol=None, ticket=None, group=None):
        response = self.stub.PositionsGet(messages_pb2.PositionsGetRequest(symbol=symbol, ticket=ticket, group=group))

        if response.error.code == 0:
            positions = tuple(map(lambda s: auto_map(s, TradePosition, 'right'), response.positions))
            return positions

        return response.error.code, response.error.message

    def history_orders_total(self, date_from, date_to):
        response = self.stub.HistoryOrdersTotal(
            messages_pb2.HistoryOrdersTotalRequest(date_from=date_from, date_to=date_to))

        if response.error.code == 0:
            return response.total
        return response.error.code, response.error.message

    def history_orders_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        response = self.stub.HistoryOrdersGet(
            messages_pb2.HistoryOrdersGetRequest(date_from=date_from,
                                                 date_to=date_to,
                                                 ticket=ticket,
                                                 group=group,
                                                 position=position)
        )

        if response.error.code == 0:
            orders = tuple(map(lambda s: auto_map(s, TradeOrder, 'right'), response.orders))
            return orders

        return response.error.code, response.error.message

    def history_deals_total(self, date_from, date_to):
        response = self.stub.HistoryDealsTotal(
            messages_pb2.HistoryDealsTotalRequest(date_from=date_from, date_to=date_to))

        if response.error.code == 0:
            return response.total
        return response.error.code, response.error.message

    def history_deals_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        response = self.stub.HistoryDealsGet(
            messages_pb2.HistoryDealsGetRequest(date_from=date_from,
                                                date_to=date_to,
                                                ticket=ticket,
                                                group=group,
                                                position=position)
        )

        if response.error.code == 0:
            orders = tuple(map(lambda s: auto_map(s, TradeDeal, 'right'), response.deals))
            return orders

        return response.error.code, response.error.message

    def last_error(self):
        response = self.stub.LastError(Empty())

        return response.error.code, response.error.message

    def market_book_release(self, symbol):
        response = self.stub.MarketBookRelease(messages_pb2.MarketBookReleaseRequest(symbol=symbol))
        if response.error.code == 0:
            return response.success
        return response.error.code, response.error.message

    def market_book_get(self, symbol):
        response = self.stub.MarketBookGet(
            messages_pb2.MarketBookGetRequest(symbol=symbol)
        )

        if response.error.code == 0:
            book_infos = list(map(lambda s: auto_map(s, BookInfo, 'right'), response.book_infos))
            return book_infos

        return response.error.code, response.error.message

    def market_book_add(self, symbol):
        response = self.stub.MarketBookAdd(messages_pb2.MarketBookAddRequest(symbol=symbol))
        if response.error.code == 0:
            return response.success
        return response.error.code, response.error.message

    def initialize(self, path, server, login, password):
        response = self.stub.Initialize(messages_pb2.InitializeRequest(path=path,
                                                                       login=login,
                                                                       server=server,
                                                                       password=password))
        if response.error.code == 0:
            return response.success

        return response.error.code, response.error.message

    def login(self, server, login, password):
        response = self.stub.Login(messages_pb2.LoginRequest(login=login,
                                                             server=server,
                                                             password=password))
        if response.error.code == 0:
            return response.success

        return response.error.code, response.error.message

    def shutdown(self):
        response = self.stub.Shutdown(Empty())
        if response.error.code == 0:
            return response.success

        return response.error.code, response.error.message

    def version(self):
        response = self.stub.Version(Empty())
        if response.error.code == 0:
            return response.version.terminal_version, response.version.build, response.version.release_date

        return response.error.code, response.error.message

    def account_info(self):
        response = self.stub.AccountInfo(Empty())
        if response.error.code == 0:
            return auto_map(response.account_info, AccountInfo, 'right')

        return response.error.code, response.error.message

    def terminal_info(self):
        response = self.stub.TerminalInfo(Empty())
        if response.error.code == 0:
            return auto_map(response.terminal_info, TerminalInfo, 'right')

        return response.error.code, response.error.message

    def Close(self, symbol, *, comment=None, ticket=None):
        response: messages_pb2.CloseResponse = self.stub.Close(
            messages_pb2.CloseRequest(symbol=symbol, comment=comment, ticket=ticket)
        )
        if response.error.code == 0:
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            order_send_result = auto_map(response.order_send_result, OrderSendResult, 'right',
                                         manual={'request': map_request})

            return order_send_result

        return response.error.code, response.error.message

    def Buy(self, symbol, volume, price=None, *, comment=None, ticket=None):
        response: messages_pb2.BuyResponse = self.stub.Buy(
            messages_pb2.BuyRequest(symbol=symbol, volume=volume, price=price, comment=comment, ticket=ticket)
        )
        if response.error.code == 0:
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            order_send_result = auto_map(response.order_send_result, OrderSendResult, 'right',
                                         manual={'request': map_request})

            return order_send_result

        return response.error.code, response.error.message

    def Sell(self, symbol, volume, price=None, *, comment=None, ticket=None):
        response: messages_pb2.SellResponse = self.stub.Sell(
            messages_pb2.SellRequest(symbol=symbol, volume=volume, price=price, comment=comment, ticket=ticket)
        )
        if response.error.code == 0:
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            order_send_result = auto_map(response.order_send_result, OrderSendResult, 'right',
                                         manual={'request': map_request})

            return order_send_result

        return response.error.code, response.error.message

    def __del__(self):
        self.channel.close()
