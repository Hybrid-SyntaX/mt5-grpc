package mt5grpctest

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestPositionsGet(t *testing.T) {
	// Must have at least one open position
	resp, err := client.PositionsGet()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.NotEmpty(t, resp)
}

func TestPositionsTotal(t *testing.T) {
	// Must have at least one open position
	resp, err := client.PositionsTotal()

	assert.Nil(t, err)
	assert.NotNil(t, resp)
	assert.Greater(t, resp, int32(0))
}
