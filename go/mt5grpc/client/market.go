package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/internal/pb"
)

func (c *Client) MarketBookAdd(symbol string) (bool, error) {
	resp, err := c.api.MarketBookAdd(c.ctx, &pb.MarketBookAddRequest{Symbol: symbol})
	if err != nil {
		return false, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.Success, nil
}

func (c *Client) MarketBookGet(symbol string) (*[]types.BookInfo, error) {
	resp, err := c.api.MarketBookGet(c.ctx, &pb.MarketBookGetRequest{Symbol: symbol})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.BookInfo, []types.BookInfo](resp, func() []*pb.BookInfo {
		return resp.GetBookInfos()
	})
}

func (c *Client) MarketBookRelease(symbol string) (bool, error) {
	resp, err := c.api.MarketBookRelease(c.ctx, &pb.MarketBookReleaseRequest{Symbol: symbol})
	if err != nil {
		return false, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.Success, nil
}
