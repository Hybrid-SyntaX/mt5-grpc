package mt5grpctest

import (
	mt5grpcclient "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/client"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	"github.com/stretchr/testify/assert"
	"testing"
)

// Misc
func TestAccountInfo(t *testing.T) {
	resp, err := client.AccountInfo()
	assert.Nil(t, err)
	assert.NotNil(t, resp)
}

func TestTerminalInfo(t *testing.T) {
	resp, err := client.TerminalInfo()
	assert.Nil(t, err)
	assert.NotNil(t, resp)
}

func TestVersion(t *testing.T) {
	resp, err := client.Version()
	assert.Nil(t, err)
	assert.NotNil(t, resp)
}

func TestShutdown(t *testing.T) {
	t.Skip("Causes other tests to fail")
	resp, err := client.Shutdown()
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.True(t, resp)
}

func TestBuy(t *testing.T) {
	resp, err := client.Buy("USDJPY", 1.0,
		mt5grpcclient.BuyWithComment("Buy test"))
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestSell(t *testing.T) {
	comment := "Sell test"

	resp, err := client.Sell("USDJPY", 1.0,
		mt5grpcclient.SellWithComment(comment))
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestClose(t *testing.T) {
	comment := "Close test"

	resp, err := client.Close("USDJPY", mt5grpcclient.CloseWithComment(comment))
	assert.Nil(t, err)
	assert.NotNil(t, resp)
}

func TestLogin(t *testing.T) {

	resp, err := client.Login(
		config.MetaTrader.Login,
		config.MetaTrader.Password,
		config.MetaTrader.Server)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.True(t, resp)
}

func TestInitialize(t *testing.T) {
	resp, err := client.Initialize(
		config.MetaTrader.Path,
		config.MetaTrader.Server,
		config.MetaTrader.Login,
		config.MetaTrader.Password,
	)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.True(t, resp)
}

func TestLastError(t *testing.T) {

	resp, err := client.LastError()
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.Equal(t, enums.ErrorCode_RES_S_OK, resp.Code)
}
