package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/client"
	"log"
	"os"
)

func main() {

	data, _ := os.ReadFile("../configs.json")
	var _config client.Config
	if err := json.Unmarshal(data, &_config); err != nil {
		log.Fatal(err)
	}

	ctx := context.Background()
	mt5client, _ := client.NewClient(_config.GRPCChannel, ctx)
	info, err := mt5client.TerminalInfo()

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Balance: %f", info.Name)
	_, _ = bufio.NewReader(os.Stdin).ReadString('\n')

}
