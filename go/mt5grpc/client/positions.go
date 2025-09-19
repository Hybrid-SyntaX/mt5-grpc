package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto"
	"google.golang.org/protobuf/types/known/emptypb"
)

type PositionsGetOption func(*pb.PositionsGetRequest)

func PositionsGetWithSymbol(symbol string) PositionsGetOption {
	return func(r *pb.PositionsGetRequest) { r.Symbol = &symbol }
}
func PositionsGetWithGroup(group string) PositionsGetOption {
	return func(r *pb.PositionsGetRequest) { r.Group = &group }
}
func PositionsGetWithTicket(ticket int64) PositionsGetOption {
	return func(r *pb.PositionsGetRequest) { r.Ticket = &ticket }
}

func (c *Client) PositionsGet(opts ...PositionsGetOption) (*[]types.TradePosition, error) {
	req := &pb.PositionsGetRequest{}
	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.PositionsGet(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.TradePosition, []types.TradePosition](resp,
		func() []*pb.TradePosition {
			return resp.GetPositions()
		})
}

func (c *Client) PositionsTotal() (int32, error) {
	resp, err := c.api.PositionsTotal(c.ctx, &emptypb.Empty{})

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetTotal(), nil
}
