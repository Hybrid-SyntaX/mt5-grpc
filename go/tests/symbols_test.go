package mt5grpctest

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestSymbolsGet(t *testing.T) {
	resp, err := client.SymbolsGet()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestSymbolInfo(t *testing.T) {
	symbol := "XAUUSD"
	resp, err := client.SymbolInfo(symbol)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
	assert.Equal(t, symbol, resp.Name)
}

func TestSymbolsTotal(t *testing.T) {
	resp, err := client.SymbolsTotal()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.GreaterOrEqual(t, resp, int64(1))
}

func TestSymbolInfoTick(t *testing.T) {
	resp, err := client.SymbolInfoTick("XAUUSD")

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
}

func TestSymbolSelect(t *testing.T) {
	resp, err := client.SymbolSelect("XAUUSD")

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.True(t, resp)
}
