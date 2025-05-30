from collections import namedtuple
from dataclasses import dataclass, field
from typing import Optional, NamedTuple

from mt5_grpc.core.enums import OrderTypeFilling, OrderTime, TradeAction, BookType, OrderType, TradeReturnCode, \
    PositionType, PositionReason, OrderState, DealEntry, DealType, DealReason, AccountTradeMode, AccountMarginMode, \
    SymbolTradeMode, SymbolSwapMode, SymbolOrderGTCMode, SymbolOptionMode, SymbolOptionRight, SymbolTradeExecution, \
    SymbolCalcMode, SymbolChartMode, ErrorCode


# @dataclass
class SymbolInfo:
    custom: bool = False  # Boolean Properties
    select: bool = False
    visible: bool = False
    spread_float: bool = False
    margin_hedged_use_leg: bool = False

    chart_mode: SymbolChartMode = SymbolChartMode.SYMBOL_CHART_MODE_BID
    session_deals: int = 0
    session_buy_orders: int = 0
    session_sell_orders: int = 0
    volume: int = 0
    volumehigh: int = 0
    volumelow: int = 0
    digits: int = 0
    spread: int = 0
    ticks_bookdepth: int = 0
    trade_calc_mode: SymbolCalcMode = SymbolCalcMode.SYMBOL_CALC_MODE_CFD
    trade_mode: SymbolTradeMode = SymbolTradeMode.SYMBOL_TRADE_MODE_DISABLED
    trade_stops_level: int = 0
    trade_freeze_level: int = 0
    trade_exemode: SymbolTradeExecution = SymbolTradeExecution.SYMBOL_TRADE_EXECUTION_INSTANT
    swap_mode: SymbolSwapMode = SymbolSwapMode.SYMBOL_SWAP_MODE_POINTS
    swap_rollover3days: int = 0
    expiration_mode: int = 0
    filling_mode: int = 0
    order_mode: int = 0
    order_gtc_mode: SymbolOrderGTCMode = SymbolOrderGTCMode.SYMBOL_ORDERS_GTC
    option_mode: SymbolOptionMode = SymbolOptionMode.SYMBOL_OPTION_MODE_AMERICAN
    option_right: SymbolOptionRight = SymbolOptionRight.SYMBOL_OPTION_RIGHT_PUT

    time: int = 0  # Timestamp Properties
    start_time: int = 0
    expiration_time: int = 0

    bid: float = 0.0  # Double Properties
    bidhigh: float = 0.0
    bidlow: float = 0.0
    ask: float = 0.0
    askhigh: float = 0.0
    asklow: float = 0.0
    last: float = 0.0
    lasthigh: float = 0.0
    lastlow: float = 0.0
    volume_real: float = 0.0
    volumehigh_real: float = 0.0
    volumelow_real: float = 0.0
    option_strike: float = 0.0
    point: float = 0.0
    trade_tick_value: float = 0.0
    trade_tick_value_profit: float = 0.0
    trade_tick_value_loss: float = 0.0
    trade_tick_size: float = 0.0
    trade_contract_size: float = 0.0
    trade_accrued_interest: float = 0.0
    trade_face_value: float = 0.0
    trade_liquidity_rate: float = 0.0
    volume_min: float = 0.0
    volume_max: float = 0.0
    volume_step: float = 0.0
    volume_limit: float = 0.0
    swap_long: float = 0.0
    swap_short: float = 0.0
    margin_initial: float = 0.0
    margin_maintenance: float = 0.0
    session_volume: float = 0.0
    session_turnover: float = 0.0
    session_interest: float = 0.0
    session_buy_orders_volume: float = 0.0
    session_sell_orders_volume: float = 0.0
    session_open: float = 0.0
    session_close: float = 0.0
    session_aw: float = 0.0
    session_price_settlement: float = 0.0
    session_price_limit_min: float = 0.0
    session_price_limit_max: float = 0.0
    margin_hedged: float = 0.0
    price_change: float = 0.0
    price_volatility: float = 0.0
    price_theoretical: float = 0.0
    price_greeks_delta: float = 0.0
    price_greeks_theta: float = 0.0
    price_greeks_gamma: float = 0.0
    price_greeks_vega: float = 0.0
    price_greeks_rho: float = 0.0
    price_greeks_omega: float = 0.0
    price_sensitivity: float = 0.0

    basis: str = ''  # String Properties
    category: str = ''
    currency_base: str = ''
    currency_profit: str = ''
    currency_margin: str = ''
    bank: str = ''
    description: str = ''
    exchange: str = ''
    formula: str = ''
    isin: str = ''
    name: str = ''
    page: str = ''
    path: str = ''

    def __str__(self):
        return self.name


class Tick:
    time: int = 0
    bid: float = 0.0
    ask: float = 0.0
    last: float = 0.0
    volume: int = 0
    time_msc: int = 0
    flags: int = 0
    volume_real: float = 0.0

    def __str__(self):
        return f'Tick(time={self.time},bid={self.bid},ask={self.ask})'


@dataclass
class TradeRequest:
    action: TradeAction = TradeAction.TRADE_ACTION_UNSPECIFIED  # Action to be performed (e.g., "buy" or "sell")
    symbol: str = ''  # Trading symbol (e.g., "EURUSD")
    volume: float = 0.0  # Volume of the trade
    comment: Optional[str] = None  # Comment associated with the trade
    deviation: int = 0  # Deviation in points
    expiration: Optional[int] = None  # Expiration time
    magic: int = 0  # Magic number for the order
    order: Optional[int] = None  # Order ID
    position: Optional[int] = None  # Position ID
    position_by: Optional[int] = None  # Position ID to close
    price: Optional[float] = None  # Price at which to execute the trade
    sl: Optional[float] = None  # Stop loss price
    stoplimit: Optional[float] = None  # Stop limit price
    tp: Optional[float] = None  # Take profit price
    type: OrderType = OrderType.ORDER_TYPE_SELL  # Type of order (e.g., market, limit)
    type_filling: OrderTypeFilling = OrderTypeFilling.ORDER_FILLING_FOK  # Type of filling (e.g., fill or kill)
    type_time: OrderTime = OrderTime.ORDER_TIME_GTC  # Type of time (e.g., good till canceled)


@dataclass
class OrderSendResult:
    ask: float = 0.0  # The ask price
    bid: float = 0.0  # The bid price
    comment: str = ""  # Comment associated with the order
    deal: int = 0  # Deal ID
    order: int = 0  # Order ID
    price: float = 0.0  # Price at which the order was executed
    # request: int = 0  # Request ID
    request: TradeRequest = field(default_factory=TradeRequest)
    request_id: int = 0  # Request ID for tracking
    retcode: TradeReturnCode = TradeReturnCode.TRADE_RETCODE_UNSPECIFIED  # Return code of the order operation
    retcode_external: int = 0  # External return code
    volume: float = 0.0  # Volume of the order


@dataclass
class OrderCheckResult:
    retcode: TradeReturnCode = TradeReturnCode.TRADE_RETCODE_UNSPECIFIED  # Operation return code
    balance: float = 0.0  # Balance value after execution
    equity: float = 0.0  # Equity value after execution
    profit: float = 0.0  # Floating profit value
    margin: float = 0.0  # Margin requirements
    margin_free: float = 0.0  # Free margin after execution
    margin_level: float = 0.0  # Margin level after execution
    comment: str = ""  # Comment on check result
    request: TradeRequest = field(default_factory=TradeRequest)  # Original trade request


@dataclass
class TradeOrder:
    ticket: int = 0  # Ticket number
    time_setup: int = 0  # Setup time
    time_setup_msc: int = 0  # Setup time in milliseconds
    time_done: int = 0  # Completion time
    time_done_msc: int = 0  # Completion time in milliseconds
    time_expiration: int = 0  # Expiration time
    type: int = 0  # Order type
    type_time: int = 0  # Time type
    type_filling: int = 0  # Filling type
    state: OrderState = OrderState.ORDER_STATE_PARTIAL  # Order state
    magic: int = 0  # Magic number
    volume_current: float = 0.0  # Current volume
    price_open: float = 0.0  # Opening price
    sl: float = 0.0  # Stop loss price
    tp: float = 0.0  # Take profit price
    price_current: float = 0.0  # Current price
    symbol: str = ""  # Trading symbol
    comment: str = ""  # Comment associated with the order
    external_id: str = ""  # External ID


@dataclass
class TradePosition:
    ticket: int = 0
    symbol: str = ""
    type: PositionType = PositionType.POSITION_TYPE_BUY
    magic: int = 0
    identifier: int = 0
    external_id: str = ''
    reason: PositionReason = PositionReason.POSITION_REASON_CLIENT
    volume: float = 0.0
    price_open: float = 0.0
    sl: float = 0.0
    tp: float = 0.0
    price_current: float = 0.0
    swap: float = 0.0
    profit: float = 0.0
    comment: str = ""
    time: int = 0
    time_msc: int = 0
    time_update: int = 0
    time_update_msc: int = 0


@dataclass
class TradeDeal:
    ticket: int = 0
    symbol: str = ''
    type: DealType = field(default=DealType.DEAL_TYPE_BUY)
    entry: DealEntry = field(default=DealEntry.DEAL_ENTRY_IN)
    reason: DealReason = field(default=DealReason.DEAL_REASON_CLIENT)
    volume: float = 0.0
    price: float = 0.0
    commission: float = 0.0
    swap: float = 0.0
    profit: float = 0.0
    magic: int = 0
    order: int = 0
    position_id: int = 0
    comment: str = ''
    external_id: str = ''
    fee: float = 0.0
    time: int = 0
    time_msc: int = 0


# @dataclass
# class Error:
#     code: ErrorCode = ErrorCode.RES_S_OK
#     message: str = ''
#

class Error(NamedTuple):
    code: ErrorCode | int = ErrorCode.RES_S_OK
    message: str = 'Success'


@dataclass
class BookInfo:
    price: float = 0.0
    type: BookType = BookType.BOOK_TYPE_UNSPECIFIED
    volume: float = 0.0
    volume_dbl: float = 0.0


from dataclasses import dataclass


@dataclass
class TerminalInfo:
    build: int = 0
    codepage: int = 0
    commondata_path: str = ''
    community_account: bool = False
    community_balance: float = 0.0
    community_connection: bool = False
    company: str = ''
    connected: bool = False
    data_path: str = ''
    dlls_allowed: bool = False
    email_enabled: bool = False
    ftp_enabled: bool = False
    language: str = ''
    maxbars: int = 0
    mqid: bool = False
    name: str = ''
    notifications_enabled: bool = False
    path: str = ''
    ping_last: int = 0
    retransmission: float = 0.0
    tradeapi_disabled: bool = False
    trade_allowed: bool = False


@dataclass
class AccountInfo:
    assets: float = 0.0
    balance: float = 0.0
    commission_blocked: float = 0.0
    company: str = ''
    credit: float = 0.0
    currency: str = ''
    currency_digits: int = 0
    equity: float = 0.0
    fifo_close: bool = False
    leverage: int = 0
    liabilities: float = 0.0
    limit_orders: int = 0
    login: int = 0
    margin: float = 0.0
    margin_free: float = 0.0
    margin_initial: float = 0.0
    margin_level: float = 0.0
    margin_maintenance: float = 0.0
    margin_mode: AccountMarginMode = AccountMarginMode.ACCOUNT_MARGIN_MODE_EXCHANGE
    margin_so_call: float = 0.0
    margin_so_mode: int = 0
    margin_so_so: float = 0.0
    name: str = ''
    profit: float = 0.0
    server: str = ''
    trade_allowed: bool = False
    trade_expert: bool = False
    trade_mode: AccountTradeMode = AccountTradeMode.ACCOUNT_TRADE_MODE_DEMO


@dataclass
class Result:
    value: any
    error: Optional[Error] = None

    @property
    def is_success(self):
        return self.error is None


class Version(NamedTuple):
    terminal_version: int
    build: int
    release_date: str
