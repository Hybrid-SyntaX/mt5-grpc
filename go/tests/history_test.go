package mt5grpctest

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestHistoryOrdersTotal(t *testing.T) {
	dateTo := time.Now()
	dateFrom := dateTo.AddDate(0, 0, -10)

	resp, err := client.HistoryOrdersTotal(dateFrom, dateTo)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.GreaterOrEqual(t, int64(resp), int64(1))
}

func TestHistoryDealsTotal(t *testing.T) {
	dateTo := time.Now()
	dateFrom := dateTo.AddDate(0, 0, -10)

	resp, err := client.HistoryDealsTotal(dateFrom, dateTo)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.GreaterOrEqual(t, int64(resp), int64(1))
}

func TestHistoryOrdersGet(t *testing.T) {
	dateTo := time.Now()
	dateFrom := dateTo.AddDate(0, 0, -10)

	resp, err := client.HistoryOrdersGet(dateFrom, dateTo)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestHistoryDealsGet(t *testing.T) {
	dateTo := time.Now()
	dateFrom := dateTo.AddDate(0, 0, -10)

	resp, err := client.HistoryDealsGet(dateFrom, dateTo)

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}
