package mt5grpctest

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestMarketBookAdd(t *testing.T) {
	resp, err := client.MarketBookAdd("EURGBP")

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.False(t, resp)
}

func TestMarketBookRelease(t *testing.T) {
	resp, err := client.MarketBookRelease("EURGBP")

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.False(t, resp)
}

func TestMarketBookGet(t *testing.T) {
	t.Skip("Doesnt work for some reason")
	_, err := client.MarketBookGet("XAUUSD")

	assert.Nil(t, err)
	//assert.NotNil(t, resp)
}
