import logging

import MetaTrader5 as mt5
from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

from ..generated_proto import services_pb2_grpc, messages_pb2
from ..generated_proto.messages_pb2 import CopyRatesRangeRequest, CopyRatesResponse, Rates, Error, CopyRatesFromRequest, \
    CopyRatesFromPosRequest, CopyTicksFromRequest, CopyTicksResponse, Ticks, CopyTicksRangeRequest, SymbolsGetResponse, \
    SymbolInfoResponse, SymbolsTotalResponse, SymbolInfoTickResponse, SymbolSelectResponse, SymbolSelectRequest, \
    SymbolInfoTickRequest, SymbolInfoRequest, SymbolsGetRequest, SymbolInfo, Tick, OrderSendRequest, OrderSendResponse, \
    OrdersGetResponse, OrdersGetRequest, OrderCheckRequest, OrderCheckResponse, OrdersTotalResponse, \
    OrderCalcMarginResponse, OrderCalcProfitResponse, OrderCalcProfitRequest, OrderCalcMarginRequest, \
    PositionsGetRequest, PositionsGetResponse, PositionsTotalResponse, HistoryOrdersTotalRequest, \
    HistoryOrdersGetResponse, HistoryOrdersTotalResponse, HistoryOrdersGetRequest, HistoryDealsTotalRequest, \
    HistoryDealsTotalResponse, HistoryDealsGetRequest, HistoryDealsGetResponse, LastErrorResponse, MarketBookAddRequest, \
    MarketBookAddResponse, MarketBookGetRequest, MarketBookGetResponse, MarketBookReleaseRequest, \
    MarketBookReleaseResponse, InitializeRequest, InitializeResponse, LoginResponse, LoginRequest, ShutdownResponse, \
    VersionResponse, AccountInfoResponse, TerminalInfoResponse, Version, TerminalInfo, AccountInfo, CloseRequest, \
    CloseResponse, BuyRequest, BuyResponse, SellResponse, SellRequest
from ..util.type_mapping import auto_map


def extract_kwargs(request, fields):
    """
    Extracts keyword arguments from a gRPC request message,
    including only the fields that are explicitly set.

    Args:
        request: The gRPC request object.
        fields (List[str]): List of field names to check.

    Returns:
        Dict[str, Any]: A dictionary of set fields and their values.
    """
    return {field: getattr(request, field) for field in fields if request.HasField(field)}


class GRPCMetaTrader5Service(services_pb2_grpc.MetaTrader5ServiceServicer):
    def __init__(self, configs):
        mt5.initialize(**configs)
        terminal_info = mt5.terminal_info()
        account_info_ = mt5.account_info()
        logging.info(f'MT5 Terminal Path: {terminal_info.path}')
        logging.info(f'Account Info: (login={account_info_.login},server={account_info_.server})')

    def CopyRatesRange(self, request: CopyRatesRangeRequest, context):
        date_to = request.date_to.ToDatetime()
        date_from = request.date_from.ToDatetime()

        rates = mt5.copy_rates_range(request.symbol, request.timeframe, date_from, date_to)

        response = CopyRatesResponse(
            rates=Rates(),
            error=self.make_error_message()
        )

        if rates is None:
            return CopyRatesResponse(error=self.make_error_message())

        self._fill_rates(response.rates, rates)

        return response

    def CopyRatesFrom(self, request: CopyRatesFromRequest, context):
        count = request.count
        date_from = request.date_from.ToDatetime()

        rates = mt5.copy_rates_from(request.symbol, request.timeframe, date_from, count)

        response = CopyRatesResponse(
            rates=Rates(),
            error=self.make_error_message()
        )

        if rates is None:
            return CopyRatesResponse(error=self.make_error_message())

        self._fill_rates(response.rates, rates)

        return response

    def CopyRatesFromPos(self, request: CopyRatesFromPosRequest, context):
        count = request.count
        start_pos = request.start_pos

        rates = mt5.copy_rates_from_pos(request.symbol, request.timeframe, start_pos, count)

        response = CopyRatesResponse(
            rates=Rates(),
            error=self.make_error_message()
        )

        if rates is None:
            return CopyRatesResponse(error=self.make_error_message())

        self._fill_rates(response.rates, rates)

        return response

    def CopyTicksFrom(self, request: CopyTicksFromRequest, context):
        count = request.count
        date_from = request.date_from.ToDatetime()
        flags = request.flags

        ticks = mt5.copy_ticks_from(request.symbol, date_from, count, flags)

        response = CopyTicksResponse(
            ticks=Ticks(),
            error=self.make_error_message()
        )

        if ticks is None:
            return CopyTicksResponse(error=self.make_error_message())

        self._fill_ticks(response.ticks, ticks)

        return response

    def CopyTicksRange(self, request: CopyTicksRangeRequest, context):
        date_from = request.date_from.ToDatetime()
        date_to = request.date_to.ToDatetime()
        flags = request.flags

        ticks = mt5.copy_ticks_range(request.symbol, date_from, date_to, flags)

        response = CopyTicksResponse(
            ticks=Ticks(),
            error=self.make_error_message()
        )

        if ticks is None or len(ticks) == 0:
            return CopyTicksResponse(error=self.make_error_message())

        self._fill_ticks(response.ticks, ticks)

        return response

    # Symbols funcs
    def SymbolsGet(self, request: SymbolsGetRequest, context) -> SymbolsGetResponse:
        symbols = mt5.symbols_get(request.group)
        if symbols is None or len(symbols) == 0:
            return SymbolsGetResponse(error=self.make_error_message())

        response = SymbolsGetResponse(error=self.make_error_message())
        symbol_infos = list(map(lambda mt5_symbol_info: auto_map(mt5_symbol_info, SymbolInfo, 'left'), symbols))
        response.symbols.extend(symbol_infos)

        return response

    def SymbolInfo(self, request: SymbolInfoRequest, context) -> SymbolInfoResponse:
        symbol_info = mt5.symbol_info(request.symbol)
        if symbol_info is None:
            return SymbolInfoResponse(error=self.make_error_message())

        response = SymbolInfoResponse(symbol_info=auto_map(symbol_info, SymbolInfo, 'left'),
                                      error=self.make_error_message())
        return response

    def SymbolsTotal(self, request: Empty, context) -> SymbolsTotalResponse:
        symbols_total = mt5.symbols_total()
        if symbols_total is None:
            return SymbolsTotalResponse(error=self.make_error_message())

        response = SymbolsTotalResponse(symbols_total=symbols_total,
                                        error=self.make_error_message())
        return response

    def SymbolInfoTick(self, request: SymbolInfoTickRequest, context) -> SymbolInfoTickResponse:
        symbol_info_tick = mt5.symbol_info_tick(request.symbol)
        if symbol_info_tick is None:
            return SymbolInfoTickResponse(error=self.make_error_message())

        tick = auto_map(symbol_info_tick, Tick, 'left')
        response = SymbolInfoTickResponse(tick=tick,
                                          error=self.make_error_message())
        return response

    def SymbolSelect(self, request: SymbolSelectRequest, context) -> SymbolSelectResponse:
        result = mt5.symbol_select(request.symbol)
        if result is None:
            return SymbolSelectResponse(error=self.make_error_message())

        response = SymbolSelectResponse(success=True,
                                        error=self.make_error_message())
        return response

    def OrderSend(self, request: OrderSendRequest, context) -> OrderSendResponse:
        trade_request_dict = MessageToDict(request.trade_request, use_integers_for_enums=True)
        result = mt5.order_send(trade_request_dict)
        if result is None:
            return OrderSendResponse(error=self.make_error_message())

        order_send_result = auto_map(result, messages_pb2.OrderSendResult, 'left',
                                     manual={'request': lambda obj, field: obj.request.CopyFrom(
                                         auto_map(field, messages_pb2.TradeRequest, 'left'))})
        return OrderSendResponse(order_send_result=order_send_result,
                                 error=self.make_error_message())

    def OrderCheck(self, request: OrderCheckRequest, context) -> OrderCheckResponse:
        trade_request_dict = MessageToDict(request.trade_request, use_integers_for_enums=True)
        result = mt5.order_check(trade_request_dict)
        if result is None:
            return OrderCheckResponse(error=self.make_error_message())

        order_check_result = auto_map(result, messages_pb2.OrderCheckResult, 'left',
                                      manual={'request': lambda obj, field: obj.request.CopyFrom(
                                          auto_map(field, messages_pb2.TradeRequest, 'left'))})
        return OrderCheckResponse(order_check_result=order_check_result,
                                  error=self.make_error_message())

    def OrdersTotal(self, request: Empty, context) -> OrdersTotalResponse:
        orders_total = mt5.orders_total()
        if orders_total is None:
            return OrdersTotalResponse(error=self.make_error_message())

        return OrdersTotalResponse(total=orders_total,
                                   error=self.make_error_message())

    def OrderCalcMargin(self, request: OrderCalcMarginRequest, context) -> OrderCalcMarginResponse:
        margin = mt5.order_calc_margin(request.action, request.symbol, request.volume, request.price)
        if margin is None:
            return OrderCalcMarginResponse(error=self.make_error_message())

        return OrderCalcMarginResponse(margin=margin, error=self.make_error_message())

    def OrderCalcProfit(self, request: OrderCalcProfitRequest, context) -> OrderCalcProfitResponse:
        profit = mt5.order_calc_profit(request.action, request.symbol, request.volume, request.price_open,
                                       request.price_close)
        if profit is None:
            return OrderCalcProfitResponse(error=self.make_error_message())

        return OrderCalcProfitResponse(profit=profit,
                                       error=self.make_error_message())

    def OrdersGet(self, request: OrdersGetRequest, context) -> OrdersGetResponse:
        if request.HasField('ticket'):
            mt5_orders = mt5.orders_get(ticket=request.ticket)
        elif request.HasField('symbol'):
            mt5_orders = mt5.orders_get(symbol=request.symbol)
        elif request.HasField('group'):
            mt5_orders = mt5.orders_get(group=request.group)
        else:
            mt5_orders = mt5.orders_get()

        if mt5_orders is None:
            return OrdersGetResponse(error=self.make_error_message())

        response = OrdersGetResponse(error=self.make_error_message())

        orders = list(map(lambda o: auto_map(o, messages_pb2.TradeOrder, 'left'), mt5_orders))
        response.orders.extend(orders)

        return response

    def PositionsGet(self, request: PositionsGetRequest, context) -> PositionsGetResponse:
        if request.HasField('ticket'):
            mt5_orders = mt5.positions_get(ticket=request.ticket)
        elif request.HasField('symbol'):
            mt5_orders = mt5.positions_get(symbol=request.symbol)
        elif request.HasField('group'):
            mt5_orders = mt5.positions_get(group=request.group)
        else:
            mt5_orders = mt5.positions_get()

        if mt5_orders is None:
            return PositionsGetResponse(error=self.make_error_message())

        response = PositionsGetResponse(error=self.make_error_message())

        orders = list(map(lambda o: auto_map(o, messages_pb2.TradePosition, 'left'), mt5_orders))
        response.positions.extend(orders)

        return response

    def PositionsTotal(self, request: Empty, context) -> PositionsTotalResponse:
        position_total = mt5.positions_total()
        if position_total is None:
            return PositionsTotalResponse(error=self.make_error_message())

        return PositionsTotalResponse(total=position_total, error=self.make_error_message())

    def HistoryOrdersTotal(self, request: HistoryOrdersTotalRequest, context) -> HistoryOrdersTotalResponse:

        orders_total = mt5.history_orders_total(request.date_from.ToDatetime(),
                                                request.date_to.ToDatetime())
        if orders_total is None:
            return HistoryOrdersTotalResponse(error=self.make_error_message())

        return HistoryOrdersTotalResponse(total=orders_total, error=self.make_error_message())

    def HistoryOrdersGet(self, request: HistoryOrdersGetRequest, context) -> HistoryOrdersGetResponse:
        if request.HasField('ticket'):
            mt5_orders = mt5.history_orders_get(ticket=request.ticket)
        elif request.HasField('position'):
            mt5_orders = mt5.history_orders_get(position=request.position)
        elif request.HasField('group'):
            mt5_orders = mt5.history_orders_get(group=request.group)
        else:
            mt5_orders = mt5.history_orders_get(request.date_from.ToDatetime(), request.date_to.ToDatetime())

        if mt5_orders is None:
            return HistoryOrdersGetResponse(error=self.make_error_message())

        response = HistoryOrdersGetResponse(error=self.make_error_message())

        orders = list(map(lambda o: auto_map(o, messages_pb2.TradeOrder, 'left'), mt5_orders))
        response.orders.extend(orders)

        return response

    def HistoryDealsTotal(self, request: HistoryDealsTotalRequest, context) -> HistoryDealsTotalResponse:
        deals_total = mt5.history_deals_total(request.date_from.ToDatetime(),
                                              request.date_to.ToDatetime())
        if deals_total is None:
            return HistoryDealsTotalResponse(error=self.make_error_message())

        return HistoryDealsTotalResponse(total=deals_total, error=self.make_error_message())

    def HistoryDealsGet(self, request: HistoryDealsGetRequest, context) -> HistoryDealsGetResponse:
        if request.HasField('ticket'):
            mt5_deals = mt5.history_deals_get(ticket=request.ticket)
        elif request.HasField('position'):
            mt5_deals = mt5.history_deals_get(position=request.position)
        elif request.HasField('group'):
            mt5_deals = mt5.history_deals_get(group=request.group)
        else:
            mt5_deals = mt5.history_deals_get(request.date_from.ToDatetime(), request.date_to.ToDatetime())

        if mt5_deals is None:
            return HistoryDealsGetResponse(error=self.make_error_message())

        response = HistoryDealsGetResponse(error=self.make_error_message())

        deals = list(map(lambda o: auto_map(o, messages_pb2.TradeDeal, 'left'), mt5_deals))
        response.deals.extend(deals)

        return response

    def LastError(self, request: Empty, context) -> LastErrorResponse:
        code, message = mt5.last_error()
        error = Error(code=code, message=message)
        return LastErrorResponse(error=error)

    def MarketBookAdd(self, request: MarketBookAddRequest, context) -> MarketBookAddResponse:
        result = mt5.market_book_add(request.symbol)

        if result is None:
            return MarketBookAddResponse(error=self.make_error_message())

        response = MarketBookAddResponse(success=result, error=self.make_error_message())
        return response

    def MarketBookGet(self, request: MarketBookGetRequest, context) -> MarketBookGetResponse:
        mt5_book_infos = mt5.market_book_get(request.symbol)

        if mt5_book_infos is None:
            return MarketBookGetResponse(error=self.make_error_message())

        response = MarketBookGetResponse(error=self.make_error_message())

        book_infos = list(map(lambda o: auto_map(o, messages_pb2.TradeDeal, 'left'), mt5_book_infos))
        response.book_infos.extend(book_infos)

        return response

    def MarketBookRelease(self, request: MarketBookReleaseRequest, context) -> MarketBookReleaseResponse:
        result = mt5.market_book_release(request.symbol)

        if result is None:
            return MarketBookReleaseResponse(error=self.make_error_message())

        response = MarketBookReleaseResponse(success=result, error=self.make_error_message())
        return response

    def Initialize(self, request: InitializeRequest, context) -> InitializeResponse:
        result = mt5.initialize(path=request.path, login=request.login, server=request.server,
                                password=request.password)

        if result is None:
            return InitializeResponse(error=self.make_error_message())

        response = InitializeResponse(success=result, error=self.make_error_message())
        return response

    def Login(self, request: LoginRequest, context) -> LoginResponse:
        result = mt5.login(request.login, server=request.server, password=request.password)

        if result is None:
            return LoginResponse(error=self.make_error_message())

        response = LoginResponse(success=result, error=self.make_error_message())
        return response

    def Shutdown(self, request: Empty, context) -> ShutdownResponse:
        result = mt5.shutdown()

        if result is None:
            return ShutdownResponse(error=self.make_error_message())

        response = ShutdownResponse(success=result, error=self.make_error_message())
        return response

    def Version(self, request: Empty, context) -> VersionResponse:
        result = mt5.version()

        if result is None:
            return VersionResponse(error=self.make_error_message())

        response = VersionResponse(error=self.make_error_message())
        response.version.CopyFrom(Version(terminal_version=result[0],
                                          build=result[1],
                                          release_date=result[2]))
        return response

    def AccountInfo(self, request: Empty, context) -> AccountInfoResponse:
        result = mt5.account_info()

        if result is None:
            return AccountInfoResponse(error=self.make_error_message())

        account_info = auto_map(result, AccountInfo, 'left')
        response = AccountInfoResponse(account_info=account_info, error=self.make_error_message())

        return response

    def TerminalInfo(self, request: Empty, context) -> TerminalInfoResponse:
        result = mt5.terminal_info()

        if result is None:
            return TerminalInfoResponse(error=self.make_error_message())

        terminal_info = auto_map(result, TerminalInfo, 'left')
        response = TerminalInfoResponse(terminal_info=terminal_info, error=self.make_error_message())

        return response

    def Close(self, request: CloseRequest, context) -> CloseResponse:
        kwargs = extract_kwargs(request, ['comment', 'ticket'])
        result = mt5.Close(request.symbol, **kwargs)

        if result is None:
            return CloseResponse(error=self.make_error_message())

        order_send_result = auto_map(result, messages_pb2.OrderSendResult, 'left',
                                     manual={'request': lambda obj, field: obj.request.CopyFrom(
                                         auto_map(field, messages_pb2.TradeRequest, 'left'))})

        response = CloseResponse(order_send_result=order_send_result, error=self.make_error_message())

        return response

    def Buy(self, request: BuyRequest, context) -> BuyResponse:
        kwargs = extract_kwargs(request, ['price', 'comment', 'ticket'])
        result = mt5.Buy(request.symbol, request.volume, **kwargs)

        if result is None:
            return BuyResponse(error=self.make_error_message())

        order_send_result = auto_map(result, messages_pb2.OrderSendResult, 'left',
                                     manual={'request': lambda obj, field: obj.request.CopyFrom(
                                         auto_map(field, messages_pb2.TradeRequest, 'left'))})

        response = BuyResponse(order_send_result=order_send_result, error=self.make_error_message())

        return response

    def Sell(self, request: SellRequest, context) -> SellResponse:
        kwargs = extract_kwargs(request, ['price', 'comment', 'ticket'])
        result = mt5.Sell(request.symbol, request.volume, **kwargs)

        if result is None:
            return SellResponse(error=self.make_error_message())

        order_send_result = auto_map(result, messages_pb2.OrderSendResult, 'left',
                                     manual={'request': lambda obj, field: obj.request.CopyFrom(
                                         auto_map(field, messages_pb2.TradeRequest, 'left'))})

        response = SellResponse(order_send_result=order_send_result, error=self.make_error_message())

        return response

    @classmethod
    def _fill_rates(cls, grpc_rates: Rates, mt5_rates):
        grpc_rates.time.extend(mt5_rates['time'])
        grpc_rates.high.extend(mt5_rates['high'])
        grpc_rates.open.extend(mt5_rates['open'])
        grpc_rates.close.extend(mt5_rates['close'])
        grpc_rates.low.extend(mt5_rates['low'])
        grpc_rates.real_volume.extend(mt5_rates['real_volume'])
        grpc_rates.tick_volume.extend(mt5_rates['tick_volume'])
        grpc_rates.spread.extend(mt5_rates['spread'])

    @classmethod
    def _fill_ticks(cls, grpc_ticks: Ticks, mt5_ticks):
        grpc_ticks.time.extend(mt5_ticks['time'])
        grpc_ticks.bid.extend(mt5_ticks['bid'])
        grpc_ticks.ask.extend(mt5_ticks['ask'])
        grpc_ticks.last.extend(mt5_ticks['last'])
        grpc_ticks.volume.extend(mt5_ticks['volume'])
        grpc_ticks.time_msc.extend(mt5_ticks['time_msc'])
        grpc_ticks.flags.extend(mt5_ticks['flags'])
        grpc_ticks.volume_real.extend(mt5_ticks['volume_real'])

    def make_error_message(self):
        error = mt5.last_error()
        return Error(
            code=error[0],
            message=error[1]
        )
