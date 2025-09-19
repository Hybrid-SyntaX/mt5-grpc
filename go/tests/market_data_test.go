package mt5grpctest

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestCopyRatesRange(t *testing.T) {

	fromDate := time.Date(2025, time.January, 1, 0, 0, 0, 0, time.UTC)
	toDate := time.Date(2025, time.January, 30, 0, 0, 0, 0, time.UTC)
	resp, err := client.CopyRatesRange("XAUUSD", enums.TimeFrame_TIMEFRAME_D1, fromDate, toDate)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
}

func TestCopyRatesFrom(t *testing.T) {
	fromDate := time.Date(2025, time.January, 1, 0, 0, 0, 0, time.UTC)
	resp, err := client.CopyRatesFrom("XAUUSD", enums.TimeFrame_TIMEFRAME_D1, fromDate, 10)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
	assert.Len(t, resp.Time, 10)
}

func TestCopyRatesFromPos(t *testing.T) {
	resp, err := client.CopyRatesFromPos("XAUUSD", enums.TimeFrame_TIMEFRAME_D1, 0, 10)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
	assert.Len(t, resp.Time, 10)
}

func TestCopyTicksFrom(t *testing.T) {
	fromDate := time.Date(2025, 5, 14, 0, 0, 0, 0, time.UTC)

	resp, err := client.CopyTicksFrom("XAUUSD", fromDate, 10, enums.CopyTicks_COPY_TICKS_ALL)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
	assert.Len(t, resp.Time, 10)
}

func TestCopyTicksRange(t *testing.T) {
	fromDate := time.Date(2025, 5, 14, 0, 0, 0, 0, time.UTC)
	toDate := time.Date(2025, 5, 14, 0, 1, 0, 0, time.UTC)
	resp, err := client.CopyTicksRange("XAUUSD", fromDate, toDate, enums.CopyTicks_COPY_TICKS_ALL)
	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp.Time)
}
