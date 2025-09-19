package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto"
	"github.com/jinzhu/copier"
	"google.golang.org/protobuf/types/known/emptypb"
)

func (c *Client) OrderSend(tradeRequest types.TradeRequest) (*types.OrderSendResult, error) {
	pbTradeRequest := new(pb.TradeRequest)
	err := copier.Copy(&pbTradeRequest, &tradeRequest)
	if err != nil {
		return nil, err
	}

	resp, err := c.api.OrderSend(c.ctx, &pb.OrderSendRequest{TradeRequest: pbTradeRequest})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.OrderSendResult, types.OrderSendResult](resp, func() *pb.OrderSendResult {
		return resp.GetOrderSendResult()
	})
}

func (c *Client) OrderCheck(tradeRequest types.TradeRequest) (*types.OrderCheckResult, error) {
	pbTradeRequest := new(pb.TradeRequest)
	err := copier.Copy(&pbTradeRequest, &tradeRequest)
	if err != nil {
		return nil, err
	}

	resp, err := c.api.OrderCheck(c.ctx, &pb.OrderCheckRequest{TradeRequest: pbTradeRequest})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.OrderCheckResult, types.OrderCheckResult](resp, func() *pb.OrderCheckResult {
		return resp.GetOrderCheckResult()
	})
}

func (c *Client) OrdersTotal() (int32, error) {
	resp, err := c.api.OrdersTotal(c.ctx, &emptypb.Empty{})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetTotal(), nil
}

type OrdersGetOption func(*pb.OrdersGetRequest)

func OrdersGetWithSymbol(symbol string) OrdersGetOption {
	return func(r *pb.OrdersGetRequest) { r.Symbol = &symbol }
}
func OrdersGetWithGroup(group string) OrdersGetOption {
	return func(r *pb.OrdersGetRequest) { r.Group = &group }
}
func OrdersGetWithTicket(ticket int64) OrdersGetOption {
	return func(r *pb.OrdersGetRequest) { r.Ticket = &ticket }
}

func (c *Client) OrdersGet(opts ...OrdersGetOption) (*[]types.TradeOrder, error) {
	req := &pb.OrdersGetRequest{}
	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.OrdersGet(c.ctx, req)
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[[]*pb.TradeOrder, []types.TradeOrder](resp, func() []*pb.TradeOrder {
		return resp.GetOrders()
	})
}

func (c *Client) OrderCalcMargin(
	action enums.OrderType,
	symbol string,
	volume float64,
	price float64,
) (float64, error) {

	resp, err := c.api.OrderCalcMargin(c.ctx, &pb.OrderCalcMarginRequest{
		Action: pb.OrderType(action),
		Symbol: symbol,
		Volume: volume,
		Price:  price,
	})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetMargin(), nil
}

func (c *Client) OrderCalcProfit(
	action enums.OrderType,
	symbol string,
	volume float64,
	priceOpen float64,
	priceClose float64,
) (float64, error) {

	resp, err := c.api.OrderCalcProfit(c.ctx, &pb.OrderCalcProfitRequest{
		Action:     pb.OrderType(action),
		Symbol:     symbol,
		Volume:     volume,
		PriceOpen:  priceOpen,
		PriceClose: priceClose,
	})
	if err != nil {
		return 0, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return 0, err
	}

	return resp.GetProfit(), nil
}
