package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/utils"
	"google.golang.org/protobuf/types/known/emptypb"
)

func (c *Client) SymbolsGet(group ...string) (*[]types.SymbolInfo, error) {

	grp, err := utils.SetOptional("", group)
	if err != nil {
		return nil, err
	}

	resp, err := c.api.SymbolsGet(c.ctx, &pb.SymbolsGetRequest{Group: &grp})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.SymbolInfo, []types.SymbolInfo](resp, func() []*pb.SymbolInfo {
		return resp.GetSymbols()
	})
}

func (c *Client) SymbolInfo(symbol string) (*types.SymbolInfo, error) {
	resp, err := c.api.SymbolInfo(c.ctx, &pb.SymbolInfoRequest{Symbol: symbol})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.SymbolInfo, types.SymbolInfo](resp, func() *pb.SymbolInfo {
		return resp.GetSymbolInfo()
	})
}

func (c *Client) SymbolsTotal() (int64, error) {
	resp, err := c.api.SymbolsTotal(c.ctx, &emptypb.Empty{})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetSymbolsTotal(), nil
}

func (c *Client) SymbolInfoTick(symbol string) (*types.Tick, error) {
	resp, err := c.api.SymbolInfoTick(c.ctx, &pb.SymbolInfoTickRequest{Symbol: symbol})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Tick, types.Tick](resp, func() *pb.Tick {
		return resp.GetTick()
	})
}

func (c *Client) SymbolSelect(symbol string) (bool, error) {
	resp, err := c.api.SymbolSelect(c.ctx, &pb.SymbolSelectRequest{Symbol: symbol})
	if err != nil {
		return false, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.Success, nil

}
