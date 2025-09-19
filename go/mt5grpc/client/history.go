package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto"
	"google.golang.org/protobuf/types/known/timestamppb"
	"time"
)

func (c *Client) HistoryOrdersTotal(
	dateFrom time.Time,
	dateTo time.Time,
) (int32, error) {
	resp, err := c.api.HistoryOrdersTotal(c.ctx, &pb.HistoryOrdersTotalRequest{
		DateFrom: timestamppb.New(dateFrom),
		DateTo:   timestamppb.New(dateTo),
	})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetTotal(), nil
}

type HistoryOrdersGetOption func(request *pb.HistoryOrdersGetRequest)

func HistoryOrdersGetWithGroup(group string) HistoryOrdersGetOption {
	return func(r *pb.HistoryOrdersGetRequest) { r.Group = &group }
}
func HistoryOrdersGetWithPosition(position uint64) HistoryOrdersGetOption {
	return func(r *pb.HistoryOrdersGetRequest) { r.Position = &position }
}
func HistoryOrdersGetWithTicket(ticket uint64) HistoryOrdersGetOption {
	return func(r *pb.HistoryOrdersGetRequest) { r.Ticket = &ticket }
}

func (c *Client) HistoryOrdersGet(
	dateFrom time.Time,
	dateTo time.Time,
	opts ...HistoryOrdersGetOption) (*[]types.TradeOrder, error) {

	req := &pb.HistoryOrdersGetRequest{
		DateFrom: timestamppb.New(dateFrom),
		DateTo:   timestamppb.New(dateTo),
	}
	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.HistoryOrdersGet(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.TradeOrder, []types.TradeOrder](resp, func() []*pb.TradeOrder {
		return resp.GetOrders()
	})
}

func (c *Client) HistoryDealsTotal(dateFrom time.Time, dateTo time.Time) (int32, error) {
	resp, err := c.api.HistoryDealsTotal(c.ctx, &pb.HistoryDealsTotalRequest{
		DateFrom: timestamppb.New(dateFrom),
		DateTo:   timestamppb.New(dateTo),
	})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetTotal(), nil
}

type HistoryDealsGetOption func(request *pb.HistoryDealsGetRequest)

func HistoryDealsGetWithGroup(group string) HistoryDealsGetOption {
	return func(r *pb.HistoryDealsGetRequest) { r.Group = &group }
}
func HistoryDealsGetWithPosition(position uint64) HistoryDealsGetOption {
	return func(r *pb.HistoryDealsGetRequest) { r.Position = &position }
}
func HistoryDealsGetWithTicket(ticket uint64) HistoryDealsGetOption {
	return func(r *pb.HistoryDealsGetRequest) { r.Ticket = &ticket }
}

func (c *Client) HistoryDealsGet(dateFrom time.Time,
	dateTo time.Time,
	opts ...HistoryDealsGetOption) (*[]types.TradeDeal, error) {
	req := &pb.HistoryDealsGetRequest{
		DateFrom: timestamppb.New(dateFrom),
		DateTo:   timestamppb.New(dateTo),
	}
	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.HistoryDealsGet(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.TradeDeal, []types.TradeDeal](resp, func() []*pb.TradeDeal {
		return resp.GetDeals()
	})
}
