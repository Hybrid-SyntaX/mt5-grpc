from datetime import datetime
from typing import List, Tuple, Union, Dict, Any, Callable

from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp

from mt5_grpc.core.abstracts import AbstractMetaTrader5
from mt5_grpc.core.enums import TimeFrame, CopyTicks, OrderType, GRPCMetaTrader5ReturnType, ErrorCode
from mt5_grpc.core.types import SymbolInfo, Tick, AccountInfo, TerminalInfo, TradeRequest, TradeOrder, TradeDeal, \
    OrderSendResult, OrderCheckResult, TradePosition, Error, Result, BookInfo, Version
from mt5_grpc.generated_proto import messages_pb2
from mt5_grpc.generated_proto import services_pb2_grpc
from mt5_grpc.mt5_grpc_client.mappings import ticks_to_numpy, rates_to_numpy
from mt5_grpc.util.type_mapping import auto_map


class GRPCMetaTrader5(AbstractMetaTrader5):
    stub: services_pb2_grpc.MetaTrader5ServiceStub

    def __init__(self, channel, return_type: GRPCMetaTrader5ReturnType = GRPCMetaTrader5ReturnType.VALUE_OR_ERROR):
        self.channel = channel
        self.stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)
        self.return_type = return_type

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

        return self._make_result(response, lambda r: rates_to_numpy(r.rates))

    def copy_rates_from(self, symbol: str, timeframe: TimeFrame, date_from: datetime, count: int):
        stub = services_pb2_grpc.MetaTrader5ServiceStub(self.channel)

        date_from_timestamp = Timestamp()
        date_from_timestamp.FromDatetime(date_from)

        request = messages_pb2.CopyRatesFromRequest(
            timeframe=timeframe,
            symbol=symbol,
            date_from=date_from_timestamp,
            count=count)
        response = stub.CopyRatesFrom(request)

        return self._make_result(response, lambda r: rates_to_numpy(r.rates))

    def copy_rates_from_pos(self, symbol: str, timeframe: TimeFrame, start_pos: int, count: int):
        request = messages_pb2.CopyRatesFromPosRequest(
            timeframe=timeframe,
            symbol=symbol,
            start_pos=start_pos,
            count=count
        )
        response = self.stub.CopyRatesFromPos(request)

        return self._make_result(response, lambda r: rates_to_numpy(r.rates))

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

        return self._make_result(response, lambda r: ticks_to_numpy(r.ticks))

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

        return self._make_result(response, lambda r: ticks_to_numpy(r.ticks))

    def symbols_get(self, group=None) -> List[SymbolInfo] | Tuple[int, str] | Error:
        response: messages_pb2.SymbolsGetResponse = self.stub.SymbolsGet(messages_pb2.SymbolsGetRequest(group=group))

        return self._make_result(
            response,
            lambda r: list(map(lambda s: auto_map(s, SymbolInfo, 'right'), r.symbols))
        )

    def symbol_info_tick(self, symbol: str) -> Union[Tick, Tuple[int, str]]:
        response: messages_pb2.SymbolInfoTickResponse = self.stub.SymbolInfoTick(
            messages_pb2.SymbolInfoTickRequest(symbol=symbol))

        return self._make_result(response, lambda r: auto_map(r.tick, Tick, 'right'))

    def symbol_info(self, symbol: str) -> Union[SymbolInfo, Tuple[int, str]]:
        response: messages_pb2.SymbolInfoResponse = self.stub.SymbolInfo(messages_pb2.SymbolInfoRequest(symbol=symbol))

        return self._make_result(response, lambda r: auto_map(r.symbol_info, SymbolInfo, 'right'))

    def symbol_select(self, symbol: str):
        response: messages_pb2.SymbolSelectResponse = self.stub.SymbolSelect(
            messages_pb2.SymbolSelectRequest(symbol=symbol))

        return self._make_result(response, lambda r: r.success)

    def symbols_total(self):
        response: messages_pb2.SymbolsTotalResponse = self.stub.SymbolsTotal(Empty())

        return self._make_result(response, lambda r: r.symbols_total)

    def order_send(self, request: Union[Dict, TradeRequest]):
        if type(request) is dict:
            request = TradeRequest(**request)

        trade_request = auto_map(request, messages_pb2.TradeRequest, 'left')
        response: messages_pb2.OrderSendResponse = self.stub.OrderSend(
            messages_pb2.OrderSendRequest(trade_request=trade_request))

        def map_response(r):
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            return auto_map(r.order_send_result, OrderSendResult, 'right',
                            manual={'request': map_request})

        return self._make_result(response, map_response)

    def order_check(self, request: Union[Dict, TradeRequest]):
        if type(request) is dict:
            request = TradeRequest(**request)

        trade_request = auto_map(request, messages_pb2.TradeRequest, 'left')
        response: messages_pb2.OrderCheckResponse = self.stub.OrderCheck(
            messages_pb2.OrderCheckRequest(trade_request=trade_request))

        def map_response(r):
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            return auto_map(r.order_check_result, OrderCheckResult, 'right',
                            manual={'request': map_request})

        return self._make_result(response, map_response)

    def order_calc_profit(self, action: OrderType, symbol, volume, price_open, price_close):
        response = self.stub.OrderCalcProfit(messages_pb2.OrderCalcProfitRequest(action=action,
                                                                                 symbol=symbol,
                                                                                 volume=volume,
                                                                                 price_open=price_open,
                                                                                 price_close=price_close))

        return self._make_result(response, lambda r: r.profit)

    def order_calc_margin(self, action: OrderType, symbol, volume, price):
        response = self.stub.OrderCalcMargin(messages_pb2.OrderCalcMarginRequest(action=action,
                                                                                 symbol=symbol,
                                                                                 volume=volume,
                                                                                 price=price))

        return self._make_result(response, lambda r: r.margin)

    def orders_total(self):
        response = self.stub.OrdersTotal(Empty())

        return self._make_result(response, lambda r: r.total)

    def orders_get(self, symbol=None, ticket=None, group=None):
        response = self.stub.OrdersGet(messages_pb2.OrdersGetRequest(symbol=symbol, ticket=ticket, group=group))

        return self._make_result(response, lambda r: tuple(map(lambda s: auto_map(s, TradeOrder, 'right'), r.orders)))

    def positions_total(self):
        response = self.stub.PositionsTotal(Empty())

        return self._make_result(response, lambda r: r.total)

    def positions_get(self, symbol=None, ticket=None, group=None):
        response = self.stub.PositionsGet(messages_pb2.PositionsGetRequest(symbol=symbol, ticket=ticket, group=group))

        return self._make_result(response,
                                 lambda r: tuple(map(lambda s: auto_map(s, TradePosition, 'right'), r.positions)))

    def history_orders_total(self, date_from, date_to):
        response = self.stub.HistoryOrdersTotal(
            messages_pb2.HistoryOrdersTotalRequest(date_from=date_from, date_to=date_to))

        return self._make_result(response, lambda r: r.total)

    def history_orders_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        response = self.stub.HistoryOrdersGet(
            messages_pb2.HistoryOrdersGetRequest(date_from=date_from,
                                                 date_to=date_to,
                                                 ticket=ticket,
                                                 group=group,
                                                 position=position)
        )

        return self._make_result(response, lambda r: tuple(map(lambda s: auto_map(s, TradeOrder, 'right'), r.orders)))

    def history_deals_total(self, date_from, date_to):
        response = self.stub.HistoryDealsTotal(
            messages_pb2.HistoryDealsTotalRequest(date_from=date_from, date_to=date_to))

        return self._make_result(response, lambda r: r.total)

    def history_deals_get(self, date_from=None, date_to=None, group=None, position=None, ticket=None):
        response = self.stub.HistoryDealsGet(
            messages_pb2.HistoryDealsGetRequest(date_from=date_from,
                                                date_to=date_to,
                                                ticket=ticket,
                                                group=group,
                                                position=position)
        )

        return self._make_result(response, lambda r: tuple(map(lambda s: auto_map(s, TradeDeal, 'right'), r.deals)))

    def market_book_release(self, symbol):
        response = self.stub.MarketBookRelease(messages_pb2.MarketBookReleaseRequest(symbol=symbol))

        return self._make_result(response, lambda r: r.success)

    def market_book_get(self, symbol):
        response = self.stub.MarketBookGet(
            messages_pb2.MarketBookGetRequest(symbol=symbol)
        )

        return self._make_result(response,
                                 lambda r: list(map(lambda s: auto_map(s, BookInfo, 'right'), r.book_infos))
                                 )

    def market_book_add(self, symbol):
        response = self.stub.MarketBookAdd(messages_pb2.MarketBookAddRequest(symbol=symbol))

        return self._make_result(response, lambda r: r.success)

    def initialize(self, path, server, login, password):
        response = self.stub.Initialize(messages_pb2.InitializeRequest(path=path,
                                                                       login=login,
                                                                       server=server,
                                                                       password=password))
        return self._make_result(response, lambda r: r.success)

    def login(self, server, login, password):
        response = self.stub.Login(messages_pb2.LoginRequest(login=login,
                                                             server=server,
                                                             password=password))

        return self._make_result(response, lambda r: r.success)

    def shutdown(self):
        response = self.stub.Shutdown(Empty())

        return self._make_result(response, lambda r: r.success)

    def version(self):
        response = self.stub.Version(Empty())

        def map_response(r): return Version(response.version.terminal_version, response.version.build,
                                            response.version.release_date)

        return self._make_result(response, map_response)

    def account_info(self):
        response = self.stub.AccountInfo(Empty())

        return self._make_result(response, lambda r: auto_map(r.account_info, AccountInfo, 'right'))

    def terminal_info(self):
        response = self.stub.TerminalInfo(Empty())

        return self._make_result(response, lambda r: auto_map(r.terminal_info, TerminalInfo, 'right'))
    def last_error(self):
        return self._last_error

    def Close(self, symbol, *, comment=None, ticket=None):
        response: messages_pb2.CloseResponse = self.stub.Close(
            messages_pb2.CloseRequest(symbol=symbol, comment=comment, ticket=ticket)
        )

        def map_response(r):
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            return auto_map(r.order_send_result, OrderSendResult, 'right',
                            manual={'request': map_request})

        return self._make_result(response, map_response)

    def Buy(self, symbol, volume, price=None, *, comment=None, ticket=None):
        response: messages_pb2.BuyResponse = self.stub.Buy(
            messages_pb2.BuyRequest(symbol=symbol, volume=volume, price=price, comment=comment, ticket=ticket)
        )

        def map_response(r):
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            return auto_map(r.order_send_result, OrderSendResult, 'right',
                            manual={'request': map_request})

        return self._make_result(response, map_response)

    def Sell(self, symbol, volume, price=None, *, comment=None, ticket=None):
        response: messages_pb2.SellResponse = self.stub.Sell(
            messages_pb2.SellRequest(symbol=symbol, volume=volume, price=price, comment=comment, ticket=ticket)
        )

        def map_response(r):
            def map_request(obj, field):
                obj.request = auto_map(field, TradeRequest, 'right')

            return auto_map(r.order_send_result, OrderSendResult, 'right',
                            manual={'request': map_request})

        return self._make_result(response, map_response)

    def __del__(self):
        self.channel.close()

    def _make_result(self,
                     response: Any,
                     result_func: Callable[[Any], Any]
                     ) -> Union[Any, Result, Error, Tuple[Any, Error], None]:

        """
        Converts a response into various return types depending on the specified strategy.

        :param response: The response object expected to have an 'error' attribute.
        :param result_func: A function to extract the result if there's no error.
        :return: Varies by `return_type`.
        """

        self._last_error = Error(response.error.code, response.error.message)
        result = result_func(response) if response.error.code == ErrorCode.RES_S_OK else None

        match self.return_type:
            case GRPCMetaTrader5ReturnType.MT5_DEFAULT:
                return result
            case GRPCMetaTrader5ReturnType.RESULT:
                return Result(result, self._last_error if result is None else None)
            case GRPCMetaTrader5ReturnType.VALUE_OR_ERROR:
                return result if result is not None else self._last_error
            case GRPCMetaTrader5ReturnType.VALUE_AND_ERROR:
                return result, self._last_error

        return None  # Fallback in case of unexpected return_type
