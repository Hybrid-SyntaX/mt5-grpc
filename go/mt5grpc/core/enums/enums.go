package enums

import "fmt"

type TimeFrame int32

const (
	TimeFrame_TIMEFRAME_UNSPECIFIED TimeFrame = 0
	TimeFrame_TIMEFRAME_M1          TimeFrame = 1
	TimeFrame_TIMEFRAME_M2          TimeFrame = 2
	TimeFrame_TIMEFRAME_M3          TimeFrame = 3
	TimeFrame_TIMEFRAME_M4          TimeFrame = 4
	TimeFrame_TIMEFRAME_M5          TimeFrame = 5
	TimeFrame_TIMEFRAME_M6          TimeFrame = 6
	TimeFrame_TIMEFRAME_M10         TimeFrame = 10
	TimeFrame_TIMEFRAME_M12         TimeFrame = 12
	TimeFrame_TIMEFRAME_M15         TimeFrame = 15
	TimeFrame_TIMEFRAME_M20         TimeFrame = 20
	TimeFrame_TIMEFRAME_M30         TimeFrame = 30
	TimeFrame_TIMEFRAME_H1          TimeFrame = 16385
	TimeFrame_TIMEFRAME_H2          TimeFrame = 16386
	TimeFrame_TIMEFRAME_H3          TimeFrame = 16387
	TimeFrame_TIMEFRAME_H4          TimeFrame = 16388
	TimeFrame_TIMEFRAME_H6          TimeFrame = 16390
	TimeFrame_TIMEFRAME_H8          TimeFrame = 16392
	TimeFrame_TIMEFRAME_H12         TimeFrame = 16396
	TimeFrame_TIMEFRAME_D1          TimeFrame = 16408
	TimeFrame_TIMEFRAME_W1          TimeFrame = 32769
	TimeFrame_TIMEFRAME_MN1         TimeFrame = 49153
)

type AccountMarginMode int32

const (
	AccountMarginMode_ACCOUNT_MARGIN_MODE_RETAIL_NETTING AccountMarginMode = 0
	AccountMarginMode_ACCOUNT_MARGIN_MODE_EXCHANGE       AccountMarginMode = 1
	AccountMarginMode_ACCOUNT_MARGIN_MODE_RETAIL_HEDGING AccountMarginMode = 2
)

type AccountTradeMode int32

const (
	AccountTradeMode_ACCOUNT_TRADE_MODE_DEMO    AccountTradeMode = 0
	AccountTradeMode_ACCOUNT_TRADE_MODE_CONTEST AccountTradeMode = 1
	AccountTradeMode_ACCOUNT_TRADE_MODE_REAL    AccountTradeMode = 2
)

// ErrorCode is the integer type that holds all error values.
type ErrorCode int32

// The actual constants – they mirror the Python IntEnum exactly.
const (
	ErrorCode_RES_S_OK                    ErrorCode = 1      // generic success
	ErrorCode_RES_E_FAIL                  ErrorCode = -1     // generic fail
	ErrorCode_RES_E_INVALID_PARAMS        ErrorCode = -2     // invalid arguments/parameters
	ErrorCode_RES_E_NO_MEMORY             ErrorCode = -3     // no memory condition
	ErrorCode_RES_E_NOT_FOUND             ErrorCode = -4     // no history
	ErrorCode_RES_E_INVALID_VERSION       ErrorCode = -5     // invalid version
	ErrorCode_RES_E_AUTH_FAILED           ErrorCode = -6     // authorization failed
	ErrorCode_RES_E_UNSUPPORTED           ErrorCode = -7     // unsupported method
	ErrorCode_RES_E_AUTO_TRADING_DISABLED ErrorCode = -8     // auto‑trading disabled
	ErrorCode_RES_E_INTERNAL_FAIL         ErrorCode = -10000 // internal IPC general error
	ErrorCode_RES_E_INTERNAL_FAIL_SEND    ErrorCode = -10001 // internal IPC send failed
	ErrorCode_RES_E_INTERNAL_FAIL_RECEIVE ErrorCode = -10002 // internal IPC recv failed
	ErrorCode_RES_E_INTERNAL_FAIL_INIT    ErrorCode = -10003 // internal IPC initialization fail
	ErrorCode_RES_E_INTERNAL_FAIL_CONNECT ErrorCode = -10004 // internal IPC no ipc
	ErrorCode_RES_E_INTERNAL_FAIL_TIMEOUT ErrorCode = -10005 // internal timeout
)

// String implements fmt.Stringer so that printing an ErrorCode shows a nice name.
func (c ErrorCode) String() string {
	switch c {
	case ErrorCode_RES_S_OK:
		return "ErrorCode_RES_S_OK"
	case ErrorCode_RES_E_FAIL:
		return "ErrorCode_RES_E_FAIL"
	case ErrorCode_RES_E_INVALID_PARAMS:
		return "ErrorCode_RES_E_INVALID_PARAMS"
	case ErrorCode_RES_E_NO_MEMORY:
		return "ErrorCode_RES_E_NO_MEMORY"
	case ErrorCode_RES_E_NOT_FOUND:
		return "ErrorCode_RES_E_NOT_FOUND"
	case ErrorCode_RES_E_INVALID_VERSION:
		return "ErrorCode_RES_E_INVALID_VERSION"
	case ErrorCode_RES_E_AUTH_FAILED:
		return "ErrorCode_RES_E_AUTH_FAILED"
	case ErrorCode_RES_E_UNSUPPORTED:
		return "ErrorCode_RES_E_UNSUPPORTED"
	case ErrorCode_RES_E_AUTO_TRADING_DISABLED:
		return "ErrorCode_RES_E_AUTO_TRADING_DISABLED"
	case ErrorCode_RES_E_INTERNAL_FAIL:
		return "ErrorCode_RES_E_INTERNAL_FAIL"
	case ErrorCode_RES_E_INTERNAL_FAIL_SEND:
		return "ErrorCode_RES_E_INTERNAL_FAIL_SEND"
	case ErrorCode_RES_E_INTERNAL_FAIL_RECEIVE:
		return "ErrorCode_RES_E_INTERNAL_FAIL_RECEIVE"
	case ErrorCode_RES_E_INTERNAL_FAIL_INIT:
		return "ErrorCode_RES_E_INTERNAL_FAIL_INIT"
	case ErrorCode_RES_E_INTERNAL_FAIL_CONNECT:
		return "ErrorCode_RES_E_INTERNAL_FAIL_CONNECT"
	case ErrorCode_RES_E_INTERNAL_FAIL_TIMEOUT:
		return "ErrorCode_RES_E_INTERNAL_FAIL_TIMEOUT"
	default:
		return fmt.Sprintf("UnknownErrorCode(%d)", int32(c))
	}
}

type TickFlag int32

const (
	TickFlag_TICK_FLAG_UNSPECIFIED TickFlag = 0
	TickFlag_TICK_FLAG_BID         TickFlag = 2  // 0x02
	TickFlag_TICK_FLAG_ASK         TickFlag = 4  // 0x04
	TickFlag_TICK_FLAG_LAST        TickFlag = 8  // 0x08
	TickFlag_TICK_FLAG_VOLUME      TickFlag = 16 // 0x10
	TickFlag_TICK_FLAG_BUY         TickFlag = 32 // 0x20
	TickFlag_TICK_FLAG_SELL        TickFlag = 64 // 0x40
)

type CopyTicks int32

const (
	CopyTicks_COPY_TICKS_ALL   = -1
	CopyTicks_COPY_TICKS_INFO  = 1
	CopyTicks_COPY_TICKS_TRADE = 2
)

// ENUM_SYMBOL_CHART_MODE
type SymbolChartMode int32

const (
	SymbolChartMode_SYMBOL_CHART_MODE_BID  SymbolChartMode = 0
	SymbolChartMode_SYMBOL_CHART_MODE_LAST SymbolChartMode = 1
)

type SymbolCalcMode int32

const (
	SymbolCalcMode_SYMBOL_CALC_MODE_FOREX               SymbolCalcMode = 0
	SymbolCalcMode_SYMBOL_CALC_MODE_FUTURES             SymbolCalcMode = 1
	SymbolCalcMode_SYMBOL_CALC_MODE_CFD                 SymbolCalcMode = 2
	SymbolCalcMode_SYMBOL_CALC_MODE_CFDINDEX            SymbolCalcMode = 3
	SymbolCalcMode_SYMBOL_CALC_MODE_CFDLEVERAGE         SymbolCalcMode = 4
	SymbolCalcMode_SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE   SymbolCalcMode = 5
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_STOCKS         SymbolCalcMode = 32
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_FUTURES        SymbolCalcMode = 33
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_OPTIONS        SymbolCalcMode = 34
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_OPTIONS_MARGIN SymbolCalcMode = 36
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_BONDS          SymbolCalcMode = 37
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX    SymbolCalcMode = 38
	SymbolCalcMode_SYMBOL_CALC_MODE_EXCH_BONDS_MOEX     SymbolCalcMode = 39
	SymbolCalcMode_SYMBOL_CALC_MODE_SERV_COLLATERAL     SymbolCalcMode = 64
)

// ENUM_SYMBOL_TRADE_MODE
type SymbolTradeMode int32

const (
	SymbolTradeMode_SYMBOL_TRADE_MODE_DISABLED  SymbolTradeMode = 0
	SymbolTradeMode_SYMBOL_TRADE_MODE_LONGONLY  SymbolTradeMode = 1
	SymbolTradeMode_SYMBOL_TRADE_MODE_SHORTONLY SymbolTradeMode = 2
	SymbolTradeMode_SYMBOL_TRADE_MODE_CLOSEONLY SymbolTradeMode = 3
	SymbolTradeMode_SYMBOL_TRADE_MODE_FULL      SymbolTradeMode = 4
)

// ENUM_SYMBOL_SWAP_MODE
type SymbolSwapMode int32

const (
	SymbolSwapMode_SYMBOL_SWAP_MODE_DISABLED         SymbolSwapMode = 0
	SymbolSwapMode_SYMBOL_SWAP_MODE_POINTS           SymbolSwapMode = 1
	SymbolSwapMode_SYMBOL_SWAP_MODE_CURRENCY_SYMBOL  SymbolSwapMode = 2
	SymbolSwapMode_SYMBOL_SWAP_MODE_CURRENCY_MARGIN  SymbolSwapMode = 3
	SymbolSwapMode_SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT SymbolSwapMode = 4
	SymbolSwapMode_SYMBOL_SWAP_MODE_INTEREST_CURRENT SymbolSwapMode = 5
	SymbolSwapMode_SYMBOL_SWAP_MODE_INTEREST_OPEN    SymbolSwapMode = 6
	SymbolSwapMode_SYMBOL_SWAP_MODE_REOPEN_CURRENT   SymbolSwapMode = 7
	SymbolSwapMode_SYMBOL_SWAP_MODE_REOPEN_BID       SymbolSwapMode = 8
)

// ENUM_SYMBOL_TRADE_EXECUTION
type SymbolTradeExecution int32

const (
	SymbolTradeExecution_SYMBOL_TRADE_EXECUTION_REQUEST  SymbolTradeExecution = 0
	SymbolTradeExecution_SYMBOL_TRADE_EXECUTION_INSTANT  SymbolTradeExecution = 1
	SymbolTradeExecution_SYMBOL_TRADE_EXECUTION_MARKET   SymbolTradeExecution = 2
	SymbolTradeExecution_SYMBOL_TRADE_EXECUTION_EXCHANGE SymbolTradeExecution = 3
)

// ENUM_SYMBOL_ORDER_GTC_MODE
type SymbolOrderGTCMode int32

const (
	SymbolOrderGTCMode_SYMBOL_ORDERS_GTC            SymbolOrderGTCMode = 0
	SymbolOrderGTCMode_SYMBOL_ORDERS_DAILY          SymbolOrderGTCMode = 1
	SymbolOrderGTCMode_SYMBOL_ORDERS_DAILY_NO_STOPS SymbolOrderGTCMode = 2
)

// ENUM_SYMBOL_OPTION_MODE
type SymbolOptionMode int32

const (
	SymbolOptionMode_SYMBOL_OPTION_MODE_EUROPEAN SymbolOptionMode = 0
	SymbolOptionMode_SYMBOL_OPTION_MODE_AMERICAN SymbolOptionMode = 1
)

// ENUM_SYMBOL_OPTION_RIGHT
type SymbolOptionRight int32

const (
	SymbolOptionRight_SYMBOL_OPTION_RIGHT_CALL SymbolOptionRight = 0
	SymbolOptionRight_SYMBOL_OPTION_RIGHT_PUT  SymbolOptionRight = 1
)

type PositionType int32

const (
	PositionType_POSITION_TYPE_BUY  PositionType = 0 // Buy
	PositionType_POSITION_TYPE_SELL PositionType = 1 // Sell
)

type PositionReason int32

const (
	PositionReason_POSITION_REASON_CLIENT PositionReason = 0 // From desktop terminal
	PositionReason_POSITION_REASON_MOBILE PositionReason = 1 // From mobile app
	PositionReason_POSITION_REASON_WEB    PositionReason = 2 // From web platform
	PositionReason_POSITION_REASON_EXPERT PositionReason = 3 // From MQL5 (Expert Advisor/script)
)

type OrderState int32

const (
	OrderState_ORDER_STATE_STARTED        OrderState = 0 // Checked, not accepted
	OrderState_ORDER_STATE_PLACED         OrderState = 1 // Accepted
	OrderState_ORDER_STATE_CANCELED       OrderState = 2 // Canceled by client
	OrderState_ORDER_STATE_PARTIAL        OrderState = 3 // Partially executed
	OrderState_ORDER_STATE_FILLED         OrderState = 4 // Fully executed
	OrderState_ORDER_STATE_REJECTED       OrderState = 5 // Rejected
	OrderState_ORDER_STATE_EXPIRED        OrderState = 6 // Expired
	OrderState_ORDER_STATE_REQUEST_ADD    OrderState = 7 // Being registered
	OrderState_ORDER_STATE_REQUEST_MODIFY OrderState = 8 // Being modified
	OrderState_ORDER_STATE_REQUEST_CANCEL OrderState = 9 // Being canceled
)

type TradeAction int32

const (
	// ENUM_TRADE_REQUEST_ACTIONS, Trade Operation Types
	TradeAction_TRADE_ACTION_UNSPECIFIED TradeAction = 0
	TradeAction_TRADE_ACTION_DEAL        TradeAction = 1  // Place a trade order for an immediate execution with the specified parameters (market order)
	TradeAction_TRADE_ACTION_PENDING     TradeAction = 5  // Place a trade order for the execution under specified conditions (pending order)
	TradeAction_TRADE_ACTION_SLTP        TradeAction = 6  // Modify Stop Loss and Take Profit values of an opened position
	TradeAction_TRADE_ACTION_MODIFY      TradeAction = 7  // Modify the parameters of the order placed previously
	TradeAction_TRADE_ACTION_REMOVE      TradeAction = 8  // Delete the pending order placed previously
	TradeAction_TRADE_ACTION_CLOSE_BY    TradeAction = 10 // Close a position by an opposite one
)

type OrderType int32

const (
	// order types, ENUM_ORDER_TYPE
	OrderType_ORDER_TYPE_BUY             OrderType = 0 // Market Buy order
	OrderType_ORDER_TYPE_SELL            OrderType = 1 // Market Sell order
	OrderType_ORDER_TYPE_BUY_LIMIT       OrderType = 2 // Buy Limit pending order
	OrderType_ORDER_TYPE_SELL_LIMIT      OrderType = 3 // Sell Limit pending order
	OrderType_ORDER_TYPE_BUY_STOP        OrderType = 4 // Buy Stop pending order
	OrderType_ORDER_TYPE_SELL_STOP       OrderType = 5 // Sell Stop pending order
	OrderType_ORDER_TYPE_BUY_STOP_LIMIT  OrderType = 6 // Upon reaching the order price, a pending Buy Limit order is placed at the StopLimit price
	OrderType_ORDER_TYPE_SELL_STOP_LIMIT OrderType = 7 // Upon reaching the order price, a pending Sell Limit order is placed at the StopLimit price
	OrderType_ORDER_TYPE_CLOSE_BY        OrderType = 8 // Order to close a position by an opposite one
)

type OrderTypeFilling int32

const (
	// ENUM_ORDER_TYPE_FILLING
	OrderTypeFilling_ORDER_FILLING_FOK    OrderTypeFilling = 0 // Fill Or Kill order
	OrderTypeFilling_ORDER_FILLING_IOC    OrderTypeFilling = 1 // Immediately Or Cancel
	OrderTypeFilling_ORDER_FILLING_RETURN OrderTypeFilling = 2 // Return remaining volume to book
	OrderTypeFilling_ORDER_FILLING_BOC    OrderTypeFilling = 3 // Book Or Cancel order
)

type OrderTime int32

const (
	OrderTime_ORDER_TIME_GTC           OrderTime = 0 // Good till cancel order
	OrderTime_ORDER_TIME_DAY           OrderTime = 1 // Good till current trade day order
	OrderTime_ORDER_TIME_SPECIFIED     OrderTime = 2 // Good till expired order
	OrderTime_ORDER_TIME_SPECIFIED_DAY OrderTime = 3 // The order will be effective till 23:59:59 of the specified day. If this time is outside a trading session, the order expires in the nearest trading time.
)

type TradeReturnCode int32

const (
	TradeReturnCode_TRADE_RETCODE_UNSPECIFIED          TradeReturnCode = 0 // optional: default fallback
	TradeReturnCode_TRADE_RETCODE_REQUOTE              TradeReturnCode = 10004
	TradeReturnCode_TRADE_RETCODE_REJECT               TradeReturnCode = 10006
	TradeReturnCode_TRADE_RETCODE_CANCEL               TradeReturnCode = 10007
	TradeReturnCode_TRADE_RETCODE_PLACED               TradeReturnCode = 10008
	TradeReturnCode_TRADE_RETCODE_DONE                 TradeReturnCode = 10009
	TradeReturnCode_TRADE_RETCODE_DONE_PARTIAL         TradeReturnCode = 10010
	TradeReturnCode_TRADE_RETCODE_ERROR                TradeReturnCode = 10011
	TradeReturnCode_TRADE_RETCODE_TIMEOUT              TradeReturnCode = 10012
	TradeReturnCode_TRADE_RETCODE_INVALID              TradeReturnCode = 10013
	TradeReturnCode_TRADE_RETCODE_INVALID_VOLUME       TradeReturnCode = 10014
	TradeReturnCode_TRADE_RETCODE_INVALID_PRICE        TradeReturnCode = 10015
	TradeReturnCode_TRADE_RETCODE_INVALID_STOPS        TradeReturnCode = 10016
	TradeReturnCode_TRADE_RETCODE_TRADE_DISABLED       TradeReturnCode = 10017
	TradeReturnCode_TRADE_RETCODE_MARKET_CLOSED        TradeReturnCode = 10018
	TradeReturnCode_TRADE_RETCODE_NO_MONEY             TradeReturnCode = 10019
	TradeReturnCode_TRADE_RETCODE_PRICE_CHANGED        TradeReturnCode = 10020
	TradeReturnCode_TRADE_RETCODE_PRICE_OFF            TradeReturnCode = 10021
	TradeReturnCode_TRADE_RETCODE_INVALID_EXPIRATION   TradeReturnCode = 10022
	TradeReturnCode_TRADE_RETCODE_ORDER_CHANGED        TradeReturnCode = 10023
	TradeReturnCode_TRADE_RETCODE_TOO_MANY_REQUESTS    TradeReturnCode = 10024
	TradeReturnCode_TRADE_RETCODE_NO_CHANGES           TradeReturnCode = 10025
	TradeReturnCode_TRADE_RETCODE_SERVER_DISABLES_AT   TradeReturnCode = 10026
	TradeReturnCode_TRADE_RETCODE_CLIENT_DISABLES_AT   TradeReturnCode = 10027
	TradeReturnCode_TRADE_RETCODE_LOCKED               TradeReturnCode = 10028
	TradeReturnCode_TRADE_RETCODE_FROZEN               TradeReturnCode = 10029
	TradeReturnCode_TRADE_RETCODE_INVALID_FILL         TradeReturnCode = 10030
	TradeReturnCode_TRADE_RETCODE_CONNECTION           TradeReturnCode = 10031
	TradeReturnCode_TRADE_RETCODE_ONLY_REAL            TradeReturnCode = 10032
	TradeReturnCode_TRADE_RETCODE_LIMIT_ORDERS         TradeReturnCode = 10033
	TradeReturnCode_TRADE_RETCODE_LIMIT_VOLUME         TradeReturnCode = 10034
	TradeReturnCode_TRADE_RETCODE_INVALID_ORDER        TradeReturnCode = 10035
	TradeReturnCode_TRADE_RETCODE_POSITION_CLOSED      TradeReturnCode = 10036
	TradeReturnCode_TRADE_RETCODE_INVALID_CLOSE_VOLUME TradeReturnCode = 10038
	TradeReturnCode_TRADE_RETCODE_CLOSE_ORDER_EXIST    TradeReturnCode = 10039
	TradeReturnCode_TRADE_RETCODE_LIMIT_POSITIONS      TradeReturnCode = 10040
	TradeReturnCode_TRADE_RETCODE_REJECT_CANCEL        TradeReturnCode = 10041
	TradeReturnCode_TRADE_RETCODE_LONG_ONLY            TradeReturnCode = 10042
	TradeReturnCode_TRADE_RETCODE_SHORT_ONLY           TradeReturnCode = 10043
	TradeReturnCode_TRADE_RETCODE_CLOSE_ONLY           TradeReturnCode = 10044
	TradeReturnCode_TRADE_RETCODE_FIFO_CLOSE           TradeReturnCode = 10045
)

type DealType int32

const (
	DealType_DEAL_TYPE_BUY                      DealType = 0
	DealType_DEAL_TYPE_SELL                     DealType = 1
	DealType_DEAL_TYPE_BALANCE                  DealType = 2
	DealType_DEAL_TYPE_CREDIT                   DealType = 3
	DealType_DEAL_TYPE_CHARGE                   DealType = 4
	DealType_DEAL_TYPE_CORRECTION               DealType = 5
	DealType_DEAL_TYPE_BONUS                    DealType = 6
	DealType_DEAL_TYPE_COMMISSION               DealType = 7
	DealType_DEAL_TYPE_COMMISSION_DAILY         DealType = 8
	DealType_DEAL_TYPE_COMMISSION_MONTHLY       DealType = 9
	DealType_DEAL_TYPE_COMMISSION_AGENT_DAILY   DealType = 10
	DealType_DEAL_TYPE_COMMISSION_AGENT_MONTHLY DealType = 11
	DealType_DEAL_TYPE_INTEREST                 DealType = 12
	DealType_DEAL_TYPE_BUY_CANCELED             DealType = 13
	DealType_DEAL_TYPE_SELL_CANCELED            DealType = 14
	DealType_DEAL_DIVIDEND                      DealType = 15
	DealType_DEAL_DIVIDEND_FRANKED              DealType = 16
	DealType_DEAL_TAX                           DealType = 17
)

type DealEntry int32

const (
	DealEntry_DEAL_ENTRY_IN     DealEntry = 0
	DealEntry_DEAL_ENTRY_OUT    DealEntry = 1
	DealEntry_DEAL_ENTRY_INOUT  DealEntry = 2
	DealEntry_DEAL_ENTRY_OUT_BY DealEntry = 3
)

// ENUM_DEAL_REASON
type DealReason int32

const (
	DealReason_DEAL_REASON_CLIENT   DealReason = 0
	DealReason_DEAL_REASON_MOBILE   DealReason = 1
	DealReason_DEAL_REASON_WEB      DealReason = 2
	DealReason_DEAL_REASON_EXPERT   DealReason = 3
	DealReason_DEAL_REASON_SL       DealReason = 4
	DealReason_DEAL_REASON_TP       DealReason = 5
	DealReason_DEAL_REASON_SO       DealReason = 6
	DealReason_DEAL_REASON_ROLLOVER DealReason = 7
	DealReason_DEAL_REASON_VMARGIN  DealReason = 8
	DealReason_DEAL_REASON_SPLIT    DealReason = 9
)

type BookType int32

const (
	// ENUM_BOOK_TYPE
	BookType_BOOK_TYPE_UNSPECIFIED BookType = 0
	BookType_BOOK_TYPE_SELL        BookType = 1
	BookType_BOOK_TYPE_BUY         BookType = 2
	BookType_BOOK_TYPE_SELL_MARKET BookType = 3
	BookType_BOOK_TYPE_BUY_MARKET  BookType = 4
)
