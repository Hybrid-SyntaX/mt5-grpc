package mt5grpctest

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/utils"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestOrdersTotal(t *testing.T) {
	resp, err := client.OrdersTotal()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.Greater(t, int64(resp), int64(0))
}

func TestOrdersGet(t *testing.T) {
	// Must have at least one open order
	resp, err := client.OrdersGet()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestOrderCheck(t *testing.T) {
	tradeReq := types.TradeRequest{
		Action:      enums.TradeAction_TRADE_ACTION_DEAL,
		Magic:       123456, // int32 literal – OK
		Symbol:      utils.Ptr("USDJPY"),
		Volume:      0.01,
		Price:       utils.Ptr(1.1050),
		Sl:          utils.Ptr(0.0),
		Tp:          utils.Ptr(0.0),
		Deviation:   10, // int32 literal – OK
		Type:        enums.OrderType_ORDER_TYPE_SELL,
		TypeFilling: 0,
		TypeTime:    0,
		Comment:     utils.Ptr("test order"),
	}
	resp, err := client.OrderCheck(tradeReq)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestOrderSend(t *testing.T) {
	tradeReq := types.TradeRequest{
		Action:      enums.TradeAction_TRADE_ACTION_DEAL,
		Magic:       123456, // int32 literal – OK
		Symbol:      utils.Ptr("USDJPY"),
		Volume:      0.01,
		Price:       utils.Ptr(1.1050),
		Sl:          utils.Ptr(0.0),
		Tp:          utils.Ptr(0.0),
		Deviation:   10, // int32 literal – OK
		Type:        enums.OrderType_ORDER_TYPE_SELL,
		TypeFilling: 0,
		TypeTime:    0,
		Comment:     utils.Ptr("test order"),
	}
	resp, err := client.OrderSend(tradeReq)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestOrderCalcMargin(t *testing.T) {
	resp, err := client.OrderCalcMargin(
		enums.OrderType_ORDER_TYPE_BUY,
		"EURUSD",
		1.0,
		1.2)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestOrderCalcProfit(t *testing.T) {
	resp, err := client.OrderCalcProfit(enums.OrderType_ORDER_TYPE_BUY,
		"EURUSD",
		1.0,
		1.2,
		1.25)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}
