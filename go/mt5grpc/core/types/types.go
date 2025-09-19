package types

import (
	"fmt"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
)

type Error struct {
	Code    enums.ErrorCode
	Message string
}

func (e *Error) Error() string {
	return fmt.Sprintf("MT5 %d: %s", e.Code, e.Message)
}

type AccountInfo struct {
	Assets            float64
	Balance           float64
	CommissionBlocked float64
	Company           string
	Credit            float64
	Currency          string
	CurrencyDigits    int32
	Equity            float64
	FifoClose         int32
	Leverage          int32
	Liabilities       float64
	LimitOrders       int32
	Login             uint64
	Margin            float64
	MarginFree        float64
	MarginInitial     float64
	MarginLevel       float64
	MarginMaintenance float64
	MarginMode        enums.AccountMarginMode // same enum type, or a domain‑specific alias
	MarginSoCall      float64
	MarginSoMode      int32
	MarginSoSo        float64
	Name              string
	Profit            float64
	Server            string
	TradeAllowed      bool
	TradeExpert       bool
	TradeMode         enums.AccountTradeMode // same enum type, or a domain‑specific alias
}

type TerminalInfo struct {
	Build                int32
	Codepage             int32
	CommondataPath       string
	CommunityAccount     bool
	CommunityBalance     float64
	CommunityConnection  bool
	Company              string
	Connected            bool
	DataPath             string
	DllsAllowed          bool
	EmailEnabled         bool
	FtpEnabled           bool
	Language             string
	Maxbars              int32
	Mqid                 bool
	Name                 string
	NotificationsEnabled bool
	Path                 string
	PingLast             int32
	Retransmission       float32
	TradeapiDisabled     bool
	TradeAllowed         bool
}

type Version struct {
	TerminalVersion int32
	Build           int32
	ReleaseDate     string
}

type Rates struct {
	Time       []int64
	High       []float64
	Low        []float64
	Open       []float64
	Close      []float64
	RealVolume []float64
	TickVolume []float64
	Spread     []float64
}

type Ticks struct {
	Time       []int64
	Bid        []float64
	Ask        []float64
	Last       []float64
	Volume     []uint64
	TimeMsc    []int64
	Flags      []enums.TickFlag
	VolumeReal []float64
}

type SymbolInfo struct {
	Custom                  bool
	Select                  bool
	Visible                 bool
	SpreadFloat             bool
	MarginHedgedUseLeg      bool
	ChartMode               enums.SymbolChartMode
	SessionDeals            int32
	SessionBuyOrders        int32
	SessionSellOrders       int32
	Volume                  int32
	Volumehigh              int32
	Volumelow               int32
	Digits                  int32
	Spread                  int32
	TicksBookdepth          int32
	TradeCalcMode           enums.SymbolCalcMode
	TradeMode               enums.SymbolTradeMode
	TradeStopsLevel         int32
	TradeFreezeLevel        int32
	TradeExemode            int32
	SwapMode                enums.SymbolSwapMode
	SwapRollover3Days       int32
	ExpirationMode          enums.SymbolTradeExecution
	FillingMode             int32
	OrderMode               int32
	OrderGtcMode            enums.SymbolOrderGTCMode
	OptionMode              enums.SymbolOptionMode
	OptionRight             enums.SymbolOptionRight
	Time                    int64
	StartTime               int64
	ExpirationTime          int64
	Bid                     float64
	Bidhigh                 float64
	Bidlow                  float64
	Ask                     float64
	Askhigh                 float64
	Asklow                  float64
	Last                    float64
	Lasthigh                float64
	Lastlow                 float64
	VolumeReal              float64
	VolumehighReal          float64
	VolumelowReal           float64
	OptionStrike            float64
	Point                   float64
	TradeTickValue          float64
	TradeTickValueProfit    float64
	TradeTickValueLoss      float64
	TradeTickSize           float64
	TradeContractSize       float64
	TradeAccruedInterest    float64
	TradeFaceValue          float64
	TradeLiquidityRate      float64
	VolumeMin               float64
	VolumeMax               float64
	VolumeStep              float64
	VolumeLimit             float64
	SwapLong                float64
	SwapShort               float64
	MarginInitial           float64
	MarginMaintenance       float64
	SessionVolume           float64
	SessionTurnover         float64
	SessionInterest         float64
	SessionBuyOrdersVolume  float64
	SessionSellOrdersVolume float64
	SessionOpen             float64
	SessionClose            float64
	SessionAw               float64
	SessionPriceSettlement  float64
	SessionPriceLimitMin    float64
	SessionPriceLimitMax    float64
	MarginHedged            float64
	PriceChange             float64
	PriceVolatility         float64
	PriceTheoretical        float64
	PriceGreeksDelta        float64
	PriceGreeksTheta        float64
	PriceGreeksGamma        float64
	PriceGreeksVega         float64
	PriceGreeksRho          float64
	PriceGreeksOmega        float64
	PriceSensitivity        float64
	Basis                   string
	Category                string
	CurrencyBase            string
	CurrencyProfit          string
	CurrencyMargin          string
	Bank                    string
	Description             string
	Exchange                string
	Formula                 string
	Isin                    string
	Name                    string
	Page                    string
	Path                    string
}

type Tick struct {
	Time       int64
	Bid        float64
	Ask        float64
	Last       float64
	Volume     uint64
	TimeMsc    int64
	Flags      uint32
	VolumeReal float64
}

type TradePosition struct {
	Ticket        int64
	Symbol        string
	Type          enums.PositionType
	Magic         int32
	Identifier    int64
	ExternalId    string
	Reason        enums.PositionReason
	Volume        float64
	PriceOpen     float64
	Sl            float64
	Tp            float64
	PriceCurrent  float64
	Swap          float64
	Profit        float64
	Comment       string
	Time          int64
	TimeMsc       int64
	TimeUpdate    int64
	TimeUpdateMsc int64
}

type TradeOrder struct {
	Ticket         int64
	TimeSetup      int64
	TimeSetupMsc   int64
	TimeDone       int64
	TimeDoneMsc    int64
	TimeExpiration int64
	Type           int32
	TypeTime       int32
	TypeFilling    int32
	State          enums.OrderState
	Magic          int32
	VolumeCurrent  float64
	PriceOpen      float64
	Sl             float64
	Tp             float64
	PriceCurrent   float64
	Symbol         string
	Comment        string
	ExternalId     string
}

type TradeRequest struct {
	Action      enums.TradeAction
	Magic       int32
	Order       *int64
	Symbol      *string
	Volume      float64
	Price       *float64
	Stoplimit   *float64
	Sl          *float64
	Tp          *float64
	Deviation   int32
	Type        enums.OrderType
	TypeFilling enums.OrderTypeFilling
	TypeTime    enums.OrderTime
	Expiration  *int64
	Comment     *string
	Position    *int64
	PositionBy  *int64
}

type OrderCheckResult struct {
	Retcode     enums.TradeReturnCode
	Balance     float64
	Equity      float64
	Profit      float64
	Margin      float64
	MarginFree  float64
	MarginLevel float64
	Comment     string
	Request     *TradeRequest
}

type OrderSendResult struct {
	Ask             float64
	Bid             float64
	Comment         string
	Deal            int64
	Order           int64
	Price           float64
	Request         *TradeRequest
	RequestId       int64
	Retcode         enums.TradeReturnCode
	RetcodeExternal int32
	Volume          float64
}

type TradeDeal struct {
	Ticket     int64
	Symbol     string
	Type       enums.DealType
	Entry      enums.DealEntry
	Reason     enums.DealReason
	Volume     float64
	Price      float64
	Commission float64
	Swap       float64
	Profit     float64
	Magic      int32
	Order      int64
	PositionId int64
	Comment    string
	ExternalId string
	Fee        float64
	Time       int64
	TimeMsc    int64
}

type BookInfo struct {
	Price     float64
	Type      enums.BookType
	Volume    float64
	VolumeDbl float64
}
