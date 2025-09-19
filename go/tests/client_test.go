package mt5grpctest

import (
	"context"
	"encoding/json"
	mt5grpcclient "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/client"
	"log"
	"os"
	"testing"
)

var client *mt5grpcclient.Client
var config *mt5grpcclient.Config

func TestMain(m *testing.M) {
	ctx := context.Background()

	data, _ := os.ReadFile("../configs.json")
	var _config mt5grpcclient.Config
	if err := json.Unmarshal(data, &_config); err != nil {
		log.Fatal(err)
	}

	_client, err := mt5grpcclient.NewClient(_config.GRPCChannel, ctx)
	if err != nil {
		log.Fatal(err)
	}

	client = _client
	config = &_config

	code := m.Run()

	_client.CloseClient()

	os.Exit(code)
}
