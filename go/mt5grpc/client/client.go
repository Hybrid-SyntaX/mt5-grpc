package client

import (
	"context"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/internal/pb" // import generated proto
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/encoding/gzip"
	"log"
)

type Client struct {
	conn *grpc.ClientConn
	api  pb.MetaTrader5ServiceClient
	ctx  context.Context
}

type Config struct {
	MetaTrader  MTConfig `json:"metatrader"`
	GRPCChannel string   `json:"grpc_channel"`
}

type MTConfig struct {
	Login    int64  `json:"login"` // integer in the JSON
	Password string `json:"password"`
	Server   string `json:"server"`
	Path     string `json:"path"`
}

func NewClient(address string, ctx context.Context) (*Client, error) {
	conn, err := grpc.NewClient(address, grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultCallOptions(grpc.UseCompressor(gzip.Name)))
	if err != nil {
		return nil, err
	}
	return &Client{
		conn: conn,
		api:  pb.NewMetaTrader5ServiceClient(conn),
		ctx:  ctx,
	}, nil
}

func (c *Client) CloseClient() {
	if err := c.conn.Close(); err != nil {
		log.Printf("failed to close connection: %v", err)
	}
}
